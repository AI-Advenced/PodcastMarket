from datetime import datetime
from app import db

class Campaign(db.Model):
    """Campaign model for advertising campaigns"""
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'), nullable=False)
    
    # Campaign details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Ad type: 'pre-roll', 'mid-roll', 'post-roll', 'host-read', 'produced'
    ad_type = db.Column(db.String(50), nullable=False)
    
    # Duration and timing
    ad_duration = db.Column(db.Integer)  # Duration in seconds
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Episodes
    total_episodes = db.Column(db.Integer, default=1)
    episodes_completed = db.Column(db.Integer, default=0)
    
    # Financial
    proposed_rate = db.Column(db.Float, nullable=False)
    negotiated_rate = db.Column(db.Float)
    total_budget = db.Column(db.Float)
    
    # Content
    ad_script = db.Column(db.Text)  # Host-read script
    promo_code = db.Column(db.String(50))  # Tracking promo code
    tracking_url = db.Column(db.String(500))  # UTM tracking URL
    
    # Content approval
    content_approval_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    content_notes = db.Column(db.Text)
    
    # Status: 'draft', 'pending', 'negotiating', 'approved', 'active', 'completed', 'cancelled'
    status = db.Column(db.String(20), default='draft')
    
    # Performance goals
    target_impressions = db.Column(db.Integer)
    target_conversions = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    deals = db.relationship('Deal', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    performance = db.relationship('AdPerformance', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'brand_id': self.brand_id,
            'podcast_id': self.podcast_id,
            'title': self.title,
            'description': self.description,
            'ad_type': self.ad_type,
            'ad_duration': self.ad_duration,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_episodes': self.total_episodes,
            'episodes_completed': self.episodes_completed,
            'proposed_rate': self.proposed_rate,
            'negotiated_rate': self.negotiated_rate,
            'total_budget': self.total_budget,
            'promo_code': self.promo_code,
            'tracking_url': self.tracking_url,
            'content_approval_status': self.content_approval_status,
            'status': self.status,
            'target_impressions': self.target_impressions,
            'target_conversions': self.target_conversions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }
    
    def __repr__(self):
        return f'<Campaign {self.title}>'
