from datetime import datetime
from app import db

class Brand(db.Model):
    """Brand model"""
    __tablename__ = 'brands'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Basic information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(500))
    
    # Company details
    industry = db.Column(db.String(100))  # Tech, Fashion, Food, etc.
    company_size = db.Column(db.String(50))  # Startup, SME, Enterprise
    
    # Contact
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    
    # Target audience
    target_demographics = db.Column(db.Text)  # JSON stored as string
    
    # Budget
    monthly_budget = db.Column(db.Float)
    total_spent = db.Column(db.Float, default=0)
    
    # Preferences
    preferred_categories = db.Column(db.Text)  # JSON array of categories
    
    # Links
    website_url = db.Column(db.String(500))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaigns = db.relationship('Campaign', backref='brand', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'logo_url': self.logo_url,
            'industry': self.industry,
            'company_size': self.company_size,
            'contact_email': self.contact_email,
            'monthly_budget': self.monthly_budget,
            'total_spent': self.total_spent,
            'website_url': self.website_url,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Brand {self.name}>'
