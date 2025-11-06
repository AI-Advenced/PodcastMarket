from datetime import datetime
from app import db

class AdPerformance(db.Model):
    """Ad performance tracking model"""
    __tablename__ = 'ad_performance'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    
    # Episode information
    episode_title = db.Column(db.String(200))
    episode_date = db.Column(db.Date)
    episode_number = db.Column(db.Integer)
    
    # Metrics
    impressions = db.Column(db.Integer, default=0)  # Number of times ad was heard
    unique_listeners = db.Column(db.Integer, default=0)
    
    # Engagement metrics
    click_throughs = db.Column(db.Integer, default=0)  # Clicks on tracking URL
    promo_code_uses = db.Column(db.Integer, default=0)  # Uses of promo code
    conversions = db.Column(db.Integer, default=0)  # Actual purchases/signups
    
    # Revenue
    revenue_generated = db.Column(db.Float, default=0)
    
    # Attribution window (days)
    attribution_days = db.Column(db.Integer, default=30)
    
    # Timestamps
    tracked_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'episode_title': self.episode_title,
            'episode_date': self.episode_date.isoformat() if self.episode_date else None,
            'episode_number': self.episode_number,
            'impressions': self.impressions,
            'unique_listeners': self.unique_listeners,
            'click_throughs': self.click_throughs,
            'promo_code_uses': self.promo_code_uses,
            'conversions': self.conversions,
            'revenue_generated': self.revenue_generated,
            'tracked_date': self.tracked_date.isoformat() if self.tracked_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @property
    def ctr(self):
        """Click-through rate"""
        if self.impressions == 0:
            return 0
        return (self.click_throughs / self.impressions) * 100
    
    @property
    def conversion_rate(self):
        """Conversion rate"""
        if self.click_throughs == 0:
            return 0
        return (self.conversions / self.click_throughs) * 100
    
    @property
    def roi(self):
        """Return on investment"""
        campaign = self.campaign
        if campaign and campaign.negotiated_rate:
            cost = campaign.negotiated_rate
            if cost == 0:
                return 0
            return ((self.revenue_generated - cost) / cost) * 100
        return 0
    
    def __repr__(self):
        return f'<AdPerformance Campaign {self.campaign_id} Episode {self.episode_number}>'
