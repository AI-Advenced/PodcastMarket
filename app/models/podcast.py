from datetime import datetime
from app import db

class Podcast(db.Model):
    """Podcast model"""
    __tablename__ = 'podcasts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Basic information
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(500))
    
    # Podcast details
    category = db.Column(db.String(100))  # Technology, Business, Health, etc.
    language = db.Column(db.String(10), default='fr')
    
    # Audience metrics
    average_listeners = db.Column(db.Integer, default=0)
    total_episodes = db.Column(db.Integer, default=0)
    
    # Demographics (JSON stored as string)
    audience_demographics = db.Column(db.Text)  # Age, gender, location
    
    # Advertising info
    is_accepting_ads = db.Column(db.Boolean, default=True)
    min_rate = db.Column(db.Float)  # Minimum rate per episode
    max_rate = db.Column(db.Float)  # Maximum rate per episode
    
    # Links
    rss_feed = db.Column(db.String(500))
    apple_podcasts_url = db.Column(db.String(500))
    spotify_url = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaigns = db.relationship('Campaign', backref='podcast', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'cover_image': self.cover_image,
            'category': self.category,
            'language': self.language,
            'average_listeners': self.average_listeners,
            'total_episodes': self.total_episodes,
            'is_accepting_ads': self.is_accepting_ads,
            'min_rate': self.min_rate,
            'max_rate': self.max_rate,
            'rss_feed': self.rss_feed,
            'apple_podcasts_url': self.apple_podcasts_url,
            'spotify_url': self.spotify_url,
            'website_url': self.website_url,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Podcast {self.title}>'
