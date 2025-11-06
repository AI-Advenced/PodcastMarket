from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Podcast
from sqlalchemy import desc

podcasts_bp = Blueprint('podcasts', __name__, url_prefix='/podcasts')

@podcasts_bp.route('/')
def list_podcasts():
    """List all podcasts"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Podcast.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(
            Podcast.title.ilike(f'%{search}%') | 
            Podcast.description.ilike(f'%{search}%')
        )
    
    podcasts = query.order_by(desc(Podcast.average_listeners)).all()
    
    if request.is_json:
        return jsonify({'podcasts': [p.to_dict() for p in podcasts]}), 200
    
    return render_template('podcasts/list.html', podcasts=podcasts)

@podcasts_bp.route('/<int:podcast_id>')
def view_podcast(podcast_id):
    """View podcast details"""
    podcast = Podcast.query.get_or_404(podcast_id)
    
    if request.is_json:
        return jsonify({'podcast': podcast.to_dict()}), 200
    
    return render_template('podcasts/view.html', podcast=podcast)

@podcasts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_podcast():
    """Create new podcast"""
    if current_user.user_type != 'podcast_host':
        flash('Seuls les podcasters peuvent créer des podcasts.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        title = data.get('title')
        description = data.get('description')
        category = data.get('category')
        
        if not title:
            if request.is_json:
                return jsonify({'error': 'Title is required'}), 400
            flash('Le titre est requis.', 'danger')
            return render_template('podcasts/create.html')
        
        podcast = Podcast(
            user_id=current_user.id,
            title=title,
            description=description,
            category=category,
            cover_image=data.get('cover_image'),
            language=data.get('language', 'fr'),
            average_listeners=int(data.get('average_listeners', 0)),
            total_episodes=int(data.get('total_episodes', 0)),
            min_rate=float(data.get('min_rate', 0)) if data.get('min_rate') else None,
            max_rate=float(data.get('max_rate', 0)) if data.get('max_rate') else None,
            rss_feed=data.get('rss_feed'),
            apple_podcasts_url=data.get('apple_podcasts_url'),
            spotify_url=data.get('spotify_url'),
            website_url=data.get('website_url')
        )
        
        db.session.add(podcast)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': 'Podcast created successfully',
                'podcast': podcast.to_dict()
            }), 201
        
        flash('Podcast créé avec succès !', 'success')
        return redirect(url_for('podcasts.view_podcast', podcast_id=podcast.id))
    
    return render_template('podcasts/create.html')

@podcasts_bp.route('/<int:podcast_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_podcast(podcast_id):
    """Edit podcast"""
    podcast = Podcast.query.get_or_404(podcast_id)
    
    if podcast.user_id != current_user.id:
        flash('Vous n\'avez pas la permission de modifier ce podcast.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        podcast.title = data.get('title', podcast.title)
        podcast.description = data.get('description', podcast.description)
        podcast.category = data.get('category', podcast.category)
        podcast.cover_image = data.get('cover_image', podcast.cover_image)
        podcast.language = data.get('language', podcast.language)
        podcast.average_listeners = int(data.get('average_listeners', podcast.average_listeners))
        podcast.total_episodes = int(data.get('total_episodes', podcast.total_episodes))
        
        if data.get('min_rate'):
            podcast.min_rate = float(data.get('min_rate'))
        if data.get('max_rate'):
            podcast.max_rate = float(data.get('max_rate'))
        
        podcast.rss_feed = data.get('rss_feed', podcast.rss_feed)
        podcast.apple_podcasts_url = data.get('apple_podcasts_url', podcast.apple_podcasts_url)
        podcast.spotify_url = data.get('spotify_url', podcast.spotify_url)
        podcast.website_url = data.get('website_url', podcast.website_url)
        podcast.is_accepting_ads = data.get('is_accepting_ads', 'true').lower() == 'true'
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': 'Podcast updated successfully',
                'podcast': podcast.to_dict()
            }), 200
        
        flash('Podcast mis à jour avec succès !', 'success')
        return redirect(url_for('podcasts.view_podcast', podcast_id=podcast.id))
    
    return render_template('podcasts/edit.html', podcast=podcast)

@podcasts_bp.route('/<int:podcast_id>/delete', methods=['POST'])
@login_required
def delete_podcast(podcast_id):
    """Delete podcast"""
    podcast = Podcast.query.get_or_404(podcast_id)
    
    if podcast.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de supprimer ce podcast.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(podcast)
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': 'Podcast deleted successfully'}), 200
    
    flash('Podcast supprimé avec succès.', 'success')
    return redirect(url_for('main.dashboard'))

@podcasts_bp.route('/my')
@login_required
def my_podcasts():
    """List user's podcasts"""
    if current_user.user_type != 'podcast_host':
        flash('Seuls les podcasters peuvent accéder à cette page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    podcasts = Podcast.query.filter_by(user_id=current_user.id).order_by(desc(Podcast.created_at)).all()
    
    if request.is_json:
        return jsonify({'podcasts': [p.to_dict() for p in podcasts]}), 200
    
    return render_template('podcasts/my_podcasts.html', podcasts=podcasts)
