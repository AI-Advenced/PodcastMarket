from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import AdPerformance, Campaign, Podcast, Brand
from sqlalchemy import func, desc
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/campaign/<int:campaign_id>')
@login_required
def campaign_analytics(campaign_id):
    """View analytics for a specific campaign"""
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
        flash('Vous n\'avez pas la permission de voir ces analytics.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get all performance records for this campaign
    performance_records = AdPerformance.query.filter_by(
        campaign_id=campaign_id
    ).order_by(AdPerformance.tracked_date).all()
    
    # Calculate totals
    total_impressions = sum(p.impressions for p in performance_records)
    total_unique_listeners = sum(p.unique_listeners for p in performance_records)
    total_clicks = sum(p.click_throughs for p in performance_records)
    total_promo_uses = sum(p.promo_code_uses for p in performance_records)
    total_conversions = sum(p.conversions for p in performance_records)
    total_revenue = sum(p.revenue_generated for p in performance_records)
    
    # Calculate averages
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    
    # Calculate ROI
    campaign_cost = campaign.negotiated_rate * campaign.episodes_completed if campaign.negotiated_rate else 0
    roi = ((total_revenue - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0
    
    analytics_data = {
        'campaign': campaign.to_dict(),
        'performance_records': [p.to_dict() for p in performance_records],
        'totals': {
            'impressions': total_impressions,
            'unique_listeners': total_unique_listeners,
            'clicks': total_clicks,
            'promo_uses': total_promo_uses,
            'conversions': total_conversions,
            'revenue': total_revenue
        },
        'metrics': {
            'ctr': round(avg_ctr, 2),
            'conversion_rate': round(avg_conversion_rate, 2),
            'roi': round(roi, 2),
            'cost_per_conversion': round(campaign_cost / total_conversions, 2) if total_conversions > 0 else 0
        }
    }
    
    if request.is_json:
        return jsonify(analytics_data), 200
    
    return render_template('analytics/campaign.html', **analytics_data)

@analytics_bp.route('/podcast/<int:podcast_id>')
@login_required
def podcast_analytics(podcast_id):
    """View analytics for a podcast"""
    podcast = Podcast.query.get_or_404(podcast_id)
    
    # Check permission
    if podcast.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de voir ces analytics.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get all campaigns for this podcast
    campaigns = Campaign.query.filter_by(podcast_id=podcast_id).all()
    campaign_ids = [c.id for c in campaigns]
    
    # Get performance data
    performance_records = AdPerformance.query.filter(
        AdPerformance.campaign_id.in_(campaign_ids)
    ).all()
    
    # Calculate totals
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == 'active'])
    completed_campaigns = len([c for c in campaigns if c.status == 'completed'])
    total_revenue = sum(c.negotiated_rate * c.episodes_completed for c in campaigns if c.negotiated_rate)
    
    total_impressions = sum(p.impressions for p in performance_records)
    total_conversions = sum(p.conversions for p in performance_records)
    
    analytics_data = {
        'podcast': podcast.to_dict(),
        'campaigns': [c.to_dict() for c in campaigns],
        'totals': {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'completed_campaigns': completed_campaigns,
            'total_revenue': total_revenue,
            'total_impressions': total_impressions,
            'total_conversions': total_conversions
        }
    }
    
    if request.is_json:
        return jsonify(analytics_data), 200
    
    return render_template('analytics/podcast.html', **analytics_data)

@analytics_bp.route('/brand/<int:brand_id>')
@login_required
def brand_analytics(brand_id):
    """View analytics for a brand"""
    brand = Brand.query.get_or_404(brand_id)
    
    # Check permission
    if brand.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de voir ces analytics.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Get all campaigns for this brand
    campaigns = Campaign.query.filter_by(brand_id=brand_id).all()
    campaign_ids = [c.id for c in campaigns]
    
    # Get performance data
    performance_records = AdPerformance.query.filter(
        AdPerformance.campaign_id.in_(campaign_ids)
    ).all()
    
    # Calculate totals
    total_campaigns = len(campaigns)
    active_campaigns = len([c for c in campaigns if c.status == 'active'])
    completed_campaigns = len([c for c in campaigns if c.status == 'completed'])
    total_spent = sum(c.negotiated_rate * c.episodes_completed for c in campaigns if c.negotiated_rate)
    
    total_impressions = sum(p.impressions for p in performance_records)
    total_conversions = sum(p.conversions for p in performance_records)
    total_revenue = sum(p.revenue_generated for p in performance_records)
    
    # Calculate ROI
    roi = ((total_revenue - total_spent) / total_spent * 100) if total_spent > 0 else 0
    
    analytics_data = {
        'brand': brand.to_dict(),
        'campaigns': [c.to_dict() for c in campaigns],
        'totals': {
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'completed_campaigns': completed_campaigns,
            'total_spent': total_spent,
            'total_impressions': total_impressions,
            'total_conversions': total_conversions,
            'total_revenue': total_revenue
        },
        'metrics': {
            'roi': round(roi, 2),
            'cost_per_conversion': round(total_spent / total_conversions, 2) if total_conversions > 0 else 0,
            'average_campaign_cost': round(total_spent / total_campaigns, 2) if total_campaigns > 0 else 0
        }
    }
    
    if request.is_json:
        return jsonify(analytics_data), 200
    
    return render_template('analytics/brand.html', **analytics_data)

@analytics_bp.route('/performance/add', methods=['POST'])
@login_required
def add_performance_data():
    """Add performance tracking data"""
    data = request.form if request.form else request.get_json()
    
    campaign_id = data.get('campaign_id')
    
    if not campaign_id:
        if request.is_json:
            return jsonify({'error': 'Campaign ID required'}), 400
        flash('Campaign ID requis.', 'danger')
        return redirect(request.referrer or url_for('main.dashboard'))
    
    campaign = Campaign.query.get_or_404(campaign_id)
    
    # Check permission (podcast host can add performance data)
    if current_user.user_type != 'podcast_host' or campaign.podcast.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Seuls les podcasters peuvent ajouter des données de performance.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Create performance record
    performance = AdPerformance(
        campaign_id=campaign_id,
        episode_title=data.get('episode_title'),
        episode_date=datetime.strptime(data.get('episode_date'), '%Y-%m-%d').date() if data.get('episode_date') else None,
        episode_number=int(data.get('episode_number', 1)),
        impressions=int(data.get('impressions', 0)),
        unique_listeners=int(data.get('unique_listeners', 0)),
        click_throughs=int(data.get('click_throughs', 0)),
        promo_code_uses=int(data.get('promo_code_uses', 0)),
        conversions=int(data.get('conversions', 0)),
        revenue_generated=float(data.get('revenue_generated', 0))
    )
    
    db.session.add(performance)
    
    # Update campaign progress
    campaign.episodes_completed += 1
    
    if campaign.episodes_completed >= campaign.total_episodes:
        campaign.status = 'completed'
        campaign.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'message': 'Performance data added successfully',
            'performance': performance.to_dict()
        }), 201
    
    flash('Données de performance ajoutées avec succès.', 'success')
    return redirect(url_for('analytics.campaign_analytics', campaign_id=campaign_id))
