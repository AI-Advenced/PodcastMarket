from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models import Podcast, Brand, Campaign
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    # Get featured podcasts
    featured_podcasts = Podcast.query.filter_by(
        is_active=True, 
        is_accepting_ads=True
    ).order_by(desc(Podcast.average_listeners)).limit(6).all()
    
    return render_template('index.html', podcasts=featured_podcasts)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    if current_user.user_type == 'podcast_host':
        # Podcast host dashboard
        podcasts = Podcast.query.filter_by(user_id=current_user.id).all()
        
        # Get campaigns for user's podcasts
        podcast_ids = [p.id for p in podcasts]
        campaigns = Campaign.query.filter(
            Campaign.podcast_id.in_(podcast_ids)
        ).order_by(desc(Campaign.created_at)).limit(10).all()
        
        return render_template(
            'dashboard/podcast_host.html',
            podcasts=podcasts,
            campaigns=campaigns
        )
    
    elif current_user.user_type == 'brand':
        # Brand dashboard
        brands = Brand.query.filter_by(user_id=current_user.id).all()
        
        # Get campaigns for user's brands
        brand_ids = [b.id for b in brands]
        campaigns = Campaign.query.filter(
            Campaign.brand_id.in_(brand_ids)
        ).order_by(desc(Campaign.created_at)).limit(10).all()
        
        return render_template(
            'dashboard/brand.html',
            brands=brands,
            campaigns=campaigns
        )
    
    return render_template('dashboard/index.html')

@main_bp.route('/marketplace')
def marketplace():
    """Podcast marketplace - browse all podcasts"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Podcast.query.filter_by(is_active=True, is_accepting_ads=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            Podcast.title.ilike(f'%{search}%') | 
            Podcast.description.ilike(f'%{search}%')
        )
    
    podcasts = query.order_by(desc(Podcast.average_listeners)).all()
    
    return render_template('marketplace.html', podcasts=podcasts)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/api/stats')
@login_required
def api_stats():
    """Get user statistics"""
    if current_user.user_type == 'podcast_host':
        podcasts = Podcast.query.filter_by(user_id=current_user.id).all()
        podcast_ids = [p.id for p in podcasts]
        
        total_podcasts = len(podcasts)
        total_campaigns = Campaign.query.filter(
            Campaign.podcast_id.in_(podcast_ids)
        ).count()
        active_campaigns = Campaign.query.filter(
            Campaign.podcast_id.in_(podcast_ids),
            Campaign.status == 'active'
        ).count()
        
        total_listeners = sum(p.average_listeners for p in podcasts)
        
        return jsonify({
            'total_podcasts': total_podcasts,
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'total_listeners': total_listeners
        })
    
    elif current_user.user_type == 'brand':
        brands = Brand.query.filter_by(user_id=current_user.id).all()
        brand_ids = [b.id for b in brands]
        
        total_brands = len(brands)
        total_campaigns = Campaign.query.filter(
            Campaign.brand_id.in_(brand_ids)
        ).count()
        active_campaigns = Campaign.query.filter(
            Campaign.brand_id.in_(brand_ids),
            Campaign.status == 'active'
        ).count()
        
        total_spent = sum(b.total_spent for b in brands)
        
        return jsonify({
            'total_brands': total_brands,
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'total_spent': total_spent
        })
    
    return jsonify({'error': 'Invalid user type'}), 400
