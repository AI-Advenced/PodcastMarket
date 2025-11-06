from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Deal, Campaign
from datetime import datetime
from sqlalchemy import desc

deals_bp = Blueprint('deals', __name__, url_prefix='/deals')

@deals_bp.route('/campaign/<int:campaign_id>')
@login_required
def campaign_deals(campaign_id):
    """View all deals for a campaign"""
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission
    can_view = False
    if current_user.user_type == 'podcast_host' and campaign.podcast.user_id == current_user.id:
        can_view = True
    elif current_user.user_type == 'brand' and campaign.brand.user_id == current_user.id:
        can_view = True
    
    if not can_view:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de voir ces négociations.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    deals = Deal.query.filter_by(campaign_id=campaign_id).order_by(Deal.created_at).all()
    
    if request.is_json:
        return jsonify({
            'campaign': campaign.to_dict(),
            'deals': [d.to_dict() for d in deals]
        }), 200
    
    return render_template('deals/list.html', campaign=campaign, deals=deals)

@deals_bp.route('/create', methods=['POST'])
@login_required
def create_deal():
    """Create new deal/offer"""
    data = request.form if request.form else request.get_json()
    
    campaign_id = data.get('campaign_id')
    offered_rate = data.get('offered_rate')
    offer_type = data.get('offer_type', 'counter')
    terms = data.get('terms')
    
    if not all([campaign_id, offered_rate]):
        if request.is_json:
            return jsonify({'error': 'Missing required fields'}), 400
        flash('Tous les champs requis doivent être remplis.', 'danger')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission
    can_negotiate = False
    if current_user.user_type == 'podcast_host' and campaign.podcast.user_id == current_user.id:
        can_negotiate = True
    elif current_user.user_type == 'brand' and campaign.brand.user_id == current_user.id:
        can_negotiate = True
    
    if not can_negotiate:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de négocier cette campagne.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Create deal
    deal = Deal(
        campaign_id=campaign_id,
        from_user_id=current_user.id,
        offer_type=offer_type,
        offered_rate=float(offered_rate),
        terms=terms
    )
    
    db.session.add(deal)
    
    # Update campaign status
    campaign.status = 'negotiating'
    campaign.negotiated_rate = float(offered_rate)
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'message': 'Offer submitted successfully',
            'deal': deal.to_dict()
        }), 201
    
    flash('Offre soumise avec succès.', 'success')
    return redirect(url_for('deals.campaign_deals', campaign_id=campaign_id))

@deals_bp.route('/<int:deal_id>/respond', methods=['POST'])
@login_required
def respond_to_deal(deal_id):
    """Respond to a deal offer"""
    deal = Deal.query.get_or_404(deal_id)
    campaign = deal.campaign
    
    # Check permission (must be the other party)
    can_respond = False
    if current_user.user_type == 'podcast_host' and campaign.podcast.user_id == current_user.id and deal.from_user_id != current_user.id:
        can_respond = True
    elif current_user.user_type == 'brand' and campaign.brand.user_id == current_user.id and deal.from_user_id != current_user.id:
        can_respond = True
    
    if not can_respond:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de répondre à cette offre.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    data = request.form if request.form else request.get_json()
    response_status = data.get('response_status')
    response_message = data.get('response_message')
    
    if response_status not in ['accepted', 'rejected', 'countered']:
        if request.is_json:
            return jsonify({'error': 'Invalid response status'}), 400
        flash('Statut de réponse invalide.', 'danger')
        return redirect(url_for('deals.campaign_deals', campaign_id=campaign.id))
    
    deal.response_status = response_status
    deal.response_message = response_message
    deal.response_date = datetime.utcnow()
    
    if response_status == 'accepted':
        # Accept the deal
        campaign.negotiated_rate = deal.offered_rate
        campaign.status = 'approved'
        campaign.approved_at = datetime.utcnow()
        campaign.total_budget = campaign.negotiated_rate * campaign.total_episodes
    elif response_status == 'rejected':
        # Reject the deal
        campaign.status = 'pending'
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'message': f'Deal {response_status}',
            'deal': deal.to_dict(),
            'campaign': campaign.to_dict()
        }), 200
    
    flash(f'Offre {response_status} avec succès.', 'success')
    return redirect(url_for('deals.campaign_deals', campaign_id=campaign.id))

@deals_bp.route('/<int:deal_id>')
@login_required
def view_deal(deal_id):
    """View deal details"""
    deal = Deal.query.get_or_404(deal_id)
    campaign = deal.campaign
    
    # Check permission
    can_view = False
    if current_user.user_type == 'podcast_host' and campaign.podcast.user_id == current_user.id:
        can_view = True
    elif current_user.user_type == 'brand' and campaign.brand.user_id == current_user.id:
        can_view = True
    
    if not can_view:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de voir cette négociation.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.is_json:
        return jsonify({'deal': deal.to_dict()}), 200
    
    return render_template('deals/view.html', deal=deal, campaign=campaign)
