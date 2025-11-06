from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Campaign, Brand, Podcast
from datetime import datetime
from sqlalchemy import desc, or_

campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')

@campaigns_bp.route('/')
@login_required
def list_campaigns():
    """List user's campaigns"""
    if current_user.user_type == 'podcast_host':
        # Get campaigns for user's podcasts
        podcasts = Podcast.query.filter_by(user_id=current_user.id).all()
        podcast_ids = [p.id for p in podcasts]
        campaigns = Campaign.query.filter(
            Campaign.podcast_id.in_(podcast_ids)
        ).order_by(desc(Campaign.created_at)).all()
    
    elif current_user.user_type == 'brand':
        # Get campaigns for user's brands
        brands = Brand.query.filter_by(user_id=current_user.id).all()
        brand_ids = [b.id for b in brands]
        campaigns = Campaign.query.filter(
            Campaign.brand_id.in_(brand_ids)
        ).order_by(desc(Campaign.created_at)).all()
    else:
        campaigns = []
    
    if request.is_json:
        return jsonify({'campaigns': [c.to_dict() for c in campaigns]}), 200
    
    return render_template('campaigns/list.html', campaigns=campaigns)

@campaigns_bp.route('/<int:campaign_id>')
@login_required
def view_campaign(campaign_id):
    """View campaign details"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission
    if current_user.user_type == 'podcast_host':
        if campaign.podcast.user_id != current_user.id:
            flash('Vous n\'avez pas la permission de voir cette campagne.', 'danger')
            return redirect(url_for('main.dashboard'))
    elif current_user.user_type == 'brand':
        if campaign.brand.user_id != current_user.id:
            flash('Vous n\'avez pas la permission de voir cette campagne.', 'danger')
            return redirect(url_for('main.dashboard'))
    
    if request.is_json:
        return jsonify({'campaign': campaign.to_dict()}), 200
    
    return render_template('campaigns/view.html', campaign=campaign)

@campaigns_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    """Create new campaign"""
    if current_user.user_type != 'brand':
        flash('Seules les marques peuvent créer des campagnes.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        brand_id = data.get('brand_id')
        podcast_id = data.get('podcast_id')
        title = data.get('title')
        ad_type = data.get('ad_type')
        proposed_rate = data.get('proposed_rate')
        
        # Validation
        if not all([brand_id, podcast_id, title, ad_type, proposed_rate]):
            if request.is_json:
                return jsonify({'error': 'Missing required fields'}), 400
            flash('Tous les champs requis doivent être remplis.', 'danger')
            return render_template('campaigns/create.html')
        
        # Check brand ownership
        brand = Brand.query.get_or_404(brand_id)
        if brand.user_id != current_user.id:
            if request.is_json:
                return jsonify({'error': 'Permission denied'}), 403
            flash('Vous n\'avez pas la permission d\'utiliser cette marque.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Check podcast exists
        podcast = Podcast.query.get_or_404(podcast_id)
        
        campaign = Campaign(
            brand_id=brand_id,
            podcast_id=podcast_id,
            title=title,
            description=data.get('description'),
            ad_type=ad_type,
            ad_duration=int(data.get('ad_duration', 30)),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date() if data.get('end_date') else None,
            total_episodes=int(data.get('total_episodes', 1)),
            proposed_rate=float(proposed_rate),
            ad_script=data.get('ad_script'),
            promo_code=data.get('promo_code'),
            tracking_url=data.get('tracking_url'),
            target_impressions=int(data.get('target_impressions', 0)) if data.get('target_impressions') else None,
            target_conversions=int(data.get('target_conversions', 0)) if data.get('target_conversions') else None,
            status='pending'
        )
        
        # Calculate total budget
        campaign.total_budget = campaign.proposed_rate * campaign.total_episodes
        
        db.session.add(campaign)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': 'Campaign created successfully',
                'campaign': campaign.to_dict()
            }), 201
        
        flash('Campagne créée avec succès ! En attente de réponse du podcaster.', 'success')
        return redirect(url_for('campaigns.view_campaign', campaign_id=campaign.id))
    
    # GET request - show form
    brands = Brand.query.filter_by(user_id=current_user.id).all()
    podcasts = Podcast.query.filter_by(is_active=True, is_accepting_ads=True).all()
    
    return render_template('campaigns/create.html', brands=brands, podcasts=podcasts)

@campaigns_bp.route('/<int:campaign_id>/update-status', methods=['POST'])
@login_required
def update_status(campaign_id):
    """Update campaign status"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission (podcast host can approve/reject)
    if current_user.user_type == 'podcast_host':
        if campaign.podcast.user_id != current_user.id:
            if request.is_json:
                return jsonify({'error': 'Permission denied'}), 403
            flash('Vous n\'avez pas la permission de modifier cette campagne.', 'danger')
            return redirect(url_for('main.dashboard'))
    else:
        if request.is_json:
            return jsonify({'error': 'Only podcast hosts can update status'}), 403
        flash('Seuls les podcasters peuvent modifier le statut.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    data = request.form if request.form else request.get_json()
    new_status = data.get('status')
    
    if new_status in ['approved', 'rejected', 'negotiating']:
        campaign.status = new_status
        
        if new_status == 'approved':
            campaign.approved_at = datetime.utcnow()
            campaign.negotiated_rate = campaign.proposed_rate
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': f'Campaign {new_status}',
                'campaign': campaign.to_dict()
            }), 200
        
        flash(f'Campagne {new_status} avec succès.', 'success')
    else:
        if request.is_json:
            return jsonify({'error': 'Invalid status'}), 400
        flash('Statut invalide.', 'danger')
    
    return redirect(url_for('campaigns.view_campaign', campaign_id=campaign.id))

@campaigns_bp.route('/<int:campaign_id>/approve-content', methods=['POST'])
@login_required
def approve_content(campaign_id):
    """Approve campaign content"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission (brand can approve content)
    if current_user.user_type != 'brand' or campaign.brand.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission d\'approuver ce contenu.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    data = request.form if request.form else request.get_json()
    approval_status = data.get('approval_status')
    
    if approval_status in ['approved', 'rejected']:
        campaign.content_approval_status = approval_status
        campaign.content_notes = data.get('content_notes')
        
        if approval_status == 'approved' and campaign.status == 'approved':
            campaign.status = 'active'
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': f'Content {approval_status}',
                'campaign': campaign.to_dict()
            }), 200
        
        flash(f'Contenu {approval_status} avec succès.', 'success')
    else:
        if request.is_json:
            return jsonify({'error': 'Invalid approval status'}), 400
        flash('Statut d\'approbation invalide.', 'danger')
    
    return redirect(url_for('campaigns.view_campaign', campaign_id=campaign.id))

@campaigns_bp.route('/<int:campaign_id>/complete', methods=['POST'])
@login_required
def complete_campaign(campaign_id):
    """Mark campaign as completed"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission (podcast host marks as completed)
    if current_user.user_type == 'podcast_host':
        if campaign.podcast.user_id != current_user.id:
            if request.is_json:
                return jsonify({'error': 'Permission denied'}), 403
            flash('Vous n\'avez pas la permission de compléter cette campagne.', 'danger')
            return redirect(url_for('main.dashboard'))
    else:
        if request.is_json:
            return jsonify({'error': 'Only podcast hosts can complete campaigns'}), 403
        flash('Seuls les podcasters peuvent compléter les campagnes.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    campaign.status = 'completed'
    campaign.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'message': 'Campaign completed',
            'campaign': campaign.to_dict()
        }), 200
    
    flash('Campagne marquée comme terminée.', 'success')
    return redirect(url_for('campaigns.view_campaign', campaign_id=campaign.id))
