import os
from app import create_app, db
from app.models import User, Podcast, Brand, Campaign, Deal, AdPerformance

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make shell context for flask shell"""
    return {
        'db': db,
        'User': User,
        'Podcast': Podcast,
        'Brand': Brand,
        'Campaign': Campaign,
        'Deal': Deal,
        'AdPerformance': AdPerformance
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    # Create test users
    podcast_host = User(
        email='podcast@example.com',
        username='podcast_host',
        user_type='podcast_host',
        full_name='Jean Podcast',
        is_verified=True
    )
    podcast_host.set_password('password123')
    
    brand_user = User(
        email='brand@example.com',
        username='brand_user',
        user_type='brand',
        full_name='Marie Brand',
        company_name='TechCorp',
        is_verified=True
    )
    brand_user.set_password('password123')
    
    db.session.add(podcast_host)
    db.session.add(brand_user)
    db.session.commit()
    
    # Create sample podcast
    podcast = Podcast(
        user_id=podcast_host.id,
        title='Tech Talk France',
        description='Le podcast français sur la technologie et l\'innovation',
        category='Technology',
        language='fr',
        average_listeners=5000,
        total_episodes=50,
        min_rate=200,
        max_rate=500,
        is_accepting_ads=True,
        is_verified=True
    )
    
    db.session.add(podcast)
    db.session.commit()
    
    # Create sample brand
    brand = Brand(
        user_id=brand_user.id,
        name='TechCorp Solutions',
        description='Solutions technologiques pour entreprises',
        industry='Technology',
        company_size='SME',
        monthly_budget=5000,
        is_verified=True
    )
    
    db.session.add(brand)
    db.session.commit()
    
    # Create sample campaign
    from datetime import datetime, timedelta
    campaign = Campaign(
        brand_id=brand.id,
        podcast_id=podcast.id,
        title='TechCorp Product Launch',
        description='Campagne de lancement de notre nouveau produit',
        ad_type='host-read',
        ad_duration=60,
        start_date=(datetime.now() + timedelta(days=7)).date(),
        end_date=(datetime.now() + timedelta(days=37)).date(),
        total_episodes=4,
        proposed_rate=350,
        promo_code='TECHCORP20',
        target_impressions=20000,
        target_conversions=200,
        status='pending'
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    print('Database seeded with sample data!')
    print('Podcast Host: podcast@example.com / password123')
    print('Brand User: brand@example.com / password123')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
