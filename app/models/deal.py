from datetime import datetime
from app import db

class Deal(db.Model):
    """Deal model for negotiation history"""
    __tablename__ = 'deals'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    
    # Negotiation
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_user = db.relationship('User', foreign_keys=[from_user_id])
    
    # Offer details
    offer_type = db.Column(db.String(20), nullable=False)  # 'initial', 'counter', 'final'
    offered_rate = db.Column(db.Float, nullable=False)
    
    # Terms
    terms = db.Column(db.Text)
    
    # Response
    response_status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, countered
    response_message = db.Column(db.Text)
    response_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'from_user_id': self.from_user_id,
            'offer_type': self.offer_type,
            'offered_rate': self.offered_rate,
            'terms': self.terms,
            'response_status': self.response_status,
            'response_message': self.response_message,
            'response_date': self.response_date.isoformat() if self.response_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Deal {self.id} for Campaign {self.campaign_id}>'
