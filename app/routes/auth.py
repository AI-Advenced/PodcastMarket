from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user_type = data.get('user_type')  # 'podcast_host' or 'brand'
        full_name = data.get('full_name')
        
        # Validation
        if not all([email, username, password, user_type]):
            if request.is_json:
                return jsonify({'error': 'Missing required fields'}), 400
            flash('Tous les champs sont requis.', 'danger')
            return render_template('auth/register.html')
        
        if user_type not in ['podcast_host', 'brand']:
            if request.is_json:
                return jsonify({'error': 'Invalid user type'}), 400
            flash('Type d\'utilisateur invalide.', 'danger')
            return render_template('auth/register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'error': 'Email already registered'}), 400
            flash('Cet email est déjà enregistré.', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'error': 'Username already taken'}), 400
            flash('Ce nom d\'utilisateur est déjà pris.', 'danger')
            return render_template('auth/register.html')
        
        # Create user
        user = User(
            email=email,
            username=username,
            user_type=user_type,
            full_name=full_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        data = request.form if request.form else request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not email or not password:
            if request.is_json:
                return jsonify({'error': 'Email and password required'}), 400
            flash('Email et mot de passe requis.', 'danger')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            if request.is_json:
                return jsonify({'error': 'Invalid email or password'}), 401
            flash('Email ou mot de passe invalide.', 'danger')
            return render_template('auth/login.html')
        
        if not user.is_active:
            if request.is_json:
                return jsonify({'error': 'Account is disabled'}), 403
            flash('Ce compte est désactivé.', 'danger')
            return render_template('auth/login.html')
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        login_user(user, remember=remember)
        
        if request.is_json:
            return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
        
        flash(f'Bienvenue, {user.full_name or user.username} !', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile"""
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    data = request.form if request.form else request.get_json()
    
    current_user.full_name = data.get('full_name', current_user.full_name)
    current_user.company_name = data.get('company_name', current_user.company_name)
    current_user.bio = data.get('bio', current_user.bio)
    current_user.website = data.get('website', current_user.website)
    current_user.phone = data.get('phone', current_user.phone)
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': 'Profile updated', 'user': current_user.to_dict()}), 200
    
    flash('Profil mis à jour avec succès.', 'success')
    return redirect(url_for('auth.profile'))
