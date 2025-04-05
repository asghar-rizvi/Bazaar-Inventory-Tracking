from faker import Faker
from model import db, Store, ProductCatalog, StoreInventory
from app import app

fake = Faker()

KARACHI_LOCATIONS = [
    "Clifton", "Defence", "Gulshan-e-Iqbal", "North Nazimabad", "PECHS", 
    "Gulistan-e-Jauhar", "Malir", "Korangi", "Landhi", "Saddar", 
    "Lyari", "SITE Area", "Federal B Area", "Bahadurabad", "Tariq Road",
    "Garden East", "Garden West", "Shah Faisal Colony", "Gulzar-e-Hijri",
    "Surjani Town", "North Karachi", "New Karachi", "FB Industrial Area",
    "Orangi Town", "Liaquatabad", "Gulberg", "Azizabad", "Buffer Zone",
    "Shahra-e-Faisal", "MA Jinnah Road", "II Chundrigar Road", "DHA Phase 1-8",
    "Gulshan-e-Maymar", "Sohrab Goth", "Sachal", "Korangi Creek", "Airport Area",
    "Karachi Port Trust", "Bin Qasim", "Cantonment", "Manzoor Colony",
    "Model Colony", "Nazimabad", "Faisal Cantonment", "Kemari", "Mauripur",
    "Shershah", "SITE Super Highway", "UP Mor", "Gadap Town"
]

PAKISTANI_PRODUCTS = [
    "Basmati Rice (5kg)", "Wheat Flour (10kg)", "Sugar (5kg)", "Cooking Oil (5L)",
    "Red Chilli Powder (200g)", "Tea Leaves (250g)", "Lipton Yellow Label (100g)",
    "Nestle Milk Pack (1L)", "Everyday Tea Whitener (200g)", "National Salt (1kg)",
    "Shan Biryani Masala (100g)", "Shan Tikka Masala (100g)", "Colgate Toothpaste (120g)",
    "Lux Soap (80g)", "Lifebuoy Soap (90g)", "Surf Excel (1kg)", "Ariel (1kg)",
    "Nestle Pure Life Water (1.5L)", "Pakola (1.5L)", "7Up (1.5L)",
    "Pepsi (1.5L)", "Lays Chips (50g)", "Kurkure (50g)", "Oreo Biscuits (150g)",
    "Peek Freans Biscuits (200g)", "Tuc Crackers (100g)", "Rooh Afza (1L)",
    "Tang Orange (250g)", "Tapal Danedar (250g)", "Nescafe Classic (50g)",
    "Eggs (Dozen)", "Broiler Chicken (1kg)", "Beef (1kg)", "Mutton (1kg)",
    "Potatoes (1kg)", "Onions (1kg)", "Tomatoes (1kg)", "Bananas (Dozen)",
    "Red Apples (1kg)", "Kinnow (1kg)"
]
def create_stores(num_stores=500):
    with app.app_context():
        stores = []
        for _ in range(num_stores):
            location = fake.random_element(KARACHI_LOCATIONS)
            stores.append(Store(
                name=f"{fake.company()}",
                location=location
            ))
        # Bulk insert all stores at once
        db.session.bulk_save_objects(stores)
        db.session.commit()

def create_products():
    with app.app_context():
        products = []
        for product_name in PAKISTANI_PRODUCTS:
            products.append(ProductCatalog(
                name=product_name,
                description=fake.sentence(),
            ))
        # Bulk insert all products
        db.session.bulk_save_objects(products)
        db.session.commit()

def create_inventory_records():
    with app.app_context():
        stores = Store.query.all()
        products = ProductCatalog.query.all()
        inventory_records = []
        
        for store in stores:
            for product in products:
                base_qty = fake.random_int(0, 100)
                if "Rice" in product.name or "Flour" in product.name:
                    base_qty += 50  # Staples have more stock
                
                inventory_records.append(StoreInventory(
                    store_id=store.id,
                    product_id=product.id,
                    quantity=0 if fake.random_int(1, 5) == 1 else base_qty,
                    last_updated=fake.date_time_this_year()
                ))
        
        db.session.bulk_save_objects(inventory_records)
        db.session.commit()
        
        
if __name__ == "__main__":
    print("Generating Karachi-based inventory data")
    create_stores()
    print(f"Created {len(KARACHI_LOCATIONS)} Karachi locations across 500 stores")
    
    create_products()
    print(f"Added {len(PAKISTANI_PRODUCTS)} common Pakistani products")
    
    create_inventory_records()