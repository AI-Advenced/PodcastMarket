from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Brand
from sqlalchemy import desc

brands_bp = Blueprint('brands', __name__, url_prefix='/brands')

@brands_bp.route('/')
def list_brands():
    """List all brands"""
    brands = Brand.query.filter_by(is_active=True).order_by(desc(Brand.created_at)).all()
    
    if request.is_json:
        return jsonify({'brands': [b.to_dict() for b in brands]}), 200
    
    return render_template('brands/list.html', brands=brands)

@brands_bp.route('/<int:brand_id>')
def view_brand(brand_id):
    """View brand details"""
    brand = Brand.query.get_or_404(brand_id)
    
    if request.is_json:
        return jsonify({'brand': brand.to_dict()}), 200
    
    return render_template('brands/view.html', brand=brand)

@brands_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_brand():
    """Create new brand"""
    if current_user.user_type != 'brand':
        flash('Seules les marques peuvent créer des profils de marque.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            if request.is_json:
                return jsonify({'error': 'Name is required'}), 400
            flash('Le nom est requis.', 'danger')
            return render_template('brands/create.html')
        
        brand = Brand(
            user_id=current_user.id,
            name=name,
            description=description,
            logo_url=data.get('logo_url'),
            industry=data.get('industry'),
            company_size=data.get('company_size'),
            contact_email=data.get('contact_email', current_user.email),
            contact_phone=data.get('contact_phone'),
            monthly_budget=float(data.get('monthly_budget', 0)) if data.get('monthly_budget') else None,
            website_url=data.get('website_url')
        )
        
        db.session.add(brand)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': 'Brand created successfully',
                'brand': brand.to_dict()
            }), 201
        
        flash('Marque créée avec succès !', 'success')
        return redirect(url_for('brands.view_brand', brand_id=brand.id))
    
    return render_template('brands/create.html')

@brands_bp.route('/<int:brand_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_brand(brand_id):
    """Edit brand"""
    brand = Brand.query.get_or_404(brand_id)
    
    if brand.user_id != current_user.id:
        flash('Vous n\'avez pas la permission de modifier cette marque.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        brand.name = data.get('name', brand.name)
        brand.description = data.get('description', brand.description)
        brand.logo_url = data.get('logo_url', brand.logo_url)
        brand.industry = data.get('industry', brand.industry)
        brand.company_size = data.get('company_size', brand.company_size)
        brand.contact_email = data.get('contact_email', brand.contact_email)
        brand.contact_phone = data.get('contact_phone', brand.contact_phone)
        brand.website_url = data.get('website_url', brand.website_url)
        
        if data.get('monthly_budget'):
            brand.monthly_budget = float(data.get('monthly_budget'))
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'message': 'Brand updated successfully',
                'brand': brand.to_dict()
            }), 200
        
        flash('Marque mise à jour avec succès !', 'success')
        return redirect(url_for('brands.view_brand', brand_id=brand.id))
    
    return render_template('brands/edit.html', brand=brand)

@brands_bp.route('/<int:brand_id>/delete', methods=['POST'])
@login_required
def delete_brand(brand_id):
    """Delete brand"""
    brand = Brand.query.get_or_404(brand_id)
    
    if brand.user_id != current_user.id:
        if request.is_json:
            return jsonify({'error': 'Permission denied'}), 403
        flash('Vous n\'avez pas la permission de supprimer cette marque.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(brand)
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': 'Brand deleted successfully'}), 200
    
    flash('Marque supprimée avec succès.', 'success')
    return redirect(url_for('main.dashboard'))

@brands_bp.route('/my')
@login_required
def my_brands():
    """List user's brands"""
    if current_user.user_type != 'brand':
        flash('Seules les marques peuvent accéder à cette page.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    brands = Brand.query.filter_by(user_id=current_user.id).order_by(desc(Brand.created_at)).all()
    
    if request.is_json:
        return jsonify({'brands': [b.to_dict() for b in brands]}), 200
    
    return render_template('brands/my_brands.html', brands=brands)
