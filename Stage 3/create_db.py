from app_factory import create_app, db
from model import User, Store, ProductCatalog, StoreInventory
import os

def setup_database():
    """Create database tables and seed with initial data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(username='admin', is_admin=True)
            admin.set_password('bazaar123')
            db.session.add(admin)
            
        # Add sample stores if none exist
        if Store.query.count() == 0:
            stores = [
                Store(name='Main Store', location='Downtown'),
                Store(name='Branch Store', location='Uptown')
            ]
            db.session.add_all(stores)
        
        # Add sample products if none exist
        if ProductCatalog.query.count() == 0:
            products = [
                ProductCatalog(name='Laptop', description='High-end laptop', category='Electronics'),
                ProductCatalog(name='Desk Chair', description='Ergonomic office chair', category='Furniture'),
                ProductCatalog(name='Coffee Mug', description='Ceramic mug', category='Kitchenware')
            ]
            db.session.add_all(products)
        
        # Commit changes
        db.session.commit()
        
        # Add initial inventory data if none exists
        if StoreInventory.query.count() == 0:
            # Get the stores and products we just created
            stores = Store.query.all()
            products = ProductCatalog.query.all()
            
            # Add inventory entries for each product in each store
            inventory_items = []
            for store in stores:
                for product in products:
                    inventory_items.append(
                        StoreInventory(
                            store_id=store.id,
                            product_id=product.id,
                            quantity=100  # Initial stock of 100 for each product
                        )
                    )
            
            db.session.add_all(inventory_items)
            db.session.commit()
        
        print("Database setup complete!")

if __name__ == '__main__':
    setup_database()