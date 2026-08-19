from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://g24rupalijadhav_db_user:rupali2025@cluster0.g9ygwnl.mongodb.net/")
client = MongoClient(MONGO_URI)
db = client['kalakruti_db']
products_collection = db['products']

CATEGORIES = [
    "all", "nath", "choker", "bangles", "bugadi", 
    "earcuff", "hair accessories", "anklet", "ring",
]

def force_reset_and_seed():
    """Wipes old dummy data and loads YOUR exact 5 Nath images"""
    products_collection.delete_many({}) # Clear old entries
    
    all_products = [
        # --- NATH COLLECTION ---
        {
            "name": "RaniSaheb Nath",
            "category": "nath",
            "price": 499,
            "material": "Basra Pearls · Teardrop Stone",
            "description": "Royal handcrafted traditional Maharashtrian Ranisaheb pearl nath.",
            "stock": "IN STOCK",
            "image": "static/images/nath/RanisahebNath.png"
        },
        {
            "name": "Mrumayi Nath",
            "category": "nath",
            "price": 400,
            "material": "Gold Plated · Ruby Center Pearl",
            "description": "Classic Mrunmayi press nath with ruby red drop centerpiece.",
            "stock": "IN STOCK",
            "image": "static/images/nath/MrunmayiNath.png"
        },
        {
            "name": "Pach Kundan Nath",
            "category": "nath",
            "price": 600,
            "material": "Pachi Kundan · Green & Pink Leaf Motif",
            "description": "Elegant Pachi Kundan nath perfect matching for all sarees.",
            "stock": "IN STOCK",
            "image": "static/images/nath/PachKundanNath.png"
        },
        {
            "name": "Flower Moti Nath",
            "category": "nath",
            "price": 299,
            "material": "Red Ruby Center · Seed Pearls",
            "description": "Handmade flower design traditional pearl nath.",
            "stock": "IN STOCK",
            "image": "static/images/nath/MotiNath.png"
        },
        {
            "name": "GreenStone Kundan Nath",
            "category": "nath",
            "price": 600,
            "material": "Green Emerald Drop · CZ Stones",
            "description": "Unique green teardrop stone handmade press nath.",
            "stock": "IN STOCK",
            "image": "static/images/nath/GreenStoneKundanNath.png"
        },
        # --- CHOKER COLLECTION ---
        {
            "name": "Chandra Choker",
            "category": "choker",
            "price": 300,
            "material": "Gold Plated · Crescent Motifs & Pink Stones",
            "description": "Traditional crescent moon motif gold necklace set with matching earrings.",
            "stock": "IN STOCK",
            "image": "static/images/choker/ChandraChoker.png"
        },
        {
            "name": "Invisible Choker",
            "category": "choker",
            "price": 499,
            "material": "Delicate Wire · Pearl & Ruby Crescent Pendant",
            "description": "Minimalist delicate gold wire choker with pearl-accented pendant.",
            "stock": "IN STOCK",
            "image": "static/images/choker/InvisibleChoker.png"
        },
        {
            "name": "Chandrakala Choker",
            "category": "choker",
            "price": 500,
            "material": "Antique Gold Plated · Green Stone Drops",
            "description": "Elegant fitted temple-style choker with crescent design drops.",
            "stock": "IN STOCK",
            "image": "static/images/choker/ChandraKalaChoker.png"
        },
        {
            "name": "Parijatak Choker",
            "category": "choker",
            "price": 550,
            "material": "Handcrafted Seed Pearls · Floral Ruby Clusters",
            "description": "Floral parijat design woven pearl choker with matching Jhumkis.",
            "stock": "IN STOCK",
            "image": "static/images/choker/ParijatakChoker.png"
        },
        {
            "name": "Shreekamal Choker",
            "category": "choker",
            "price": 600,
            "material": "Green Meenakari Lotus · Kundan Work",
            "description": "Traditional lotus leaf meenakari choker with golden dori.",
            "stock": "IN STOCK",
            "image": "static/images/choker/ShreeKamalChoker.png"
        },
        # --- BANGLES COLLECTION ---
        {
            "name": "Moti Bangles with Kalire",
            "category": "bangles",
            "price": 899,
            "material": "Handcrafted Pearl Beads · Floral Ruby Hangings",
            "description": "Exquisite handcrafted pearl bangles attached with traditional hanging kalire.",
            "stock": "IN STOCK",
            "image": "static/images/bangles/MotiBangles.png"
        },
        {
            "name": "AshtaPailu Bracelet",
            "category": "bangles",
            "price": 799,
            "material": "Premium Micro Polish Finish · Gold Beads",
            "description": "Signature geometric faceted cut gold-toned bracelet type bangles.",
            "stock": "IN STOCK",
            "image": "static/images/bangles/AshtaPailuBracelet.png"
        },
        {
            "name": "Handmade Parijatak Bangles Set",
            "category": "bangles",
            "price": 1000,
            "material": "Woven Pearls · Floral Red Ruby Center",
            "description": "Set of 3 varieties of traditional handmade parijat pearl bangles.",
            "stock": "IN STOCK",
            "image": "static/images/bangles/HandmadeParijatakBanglesSet.png"
        },
        {
            "name": "Parijatak Bracelet",
            "category": "bangles",
            "price": 399,
            "material": "Adjustable Gold Chain · Pearl Floral Motif",
            "description": "Elegant adjustable length pearl flower motif bracelet.",
            "stock": "IN STOCK",
            "image": "static/images/bangles/ParijatakBangles.png"
        },
        # --- BUGADI COLLECTION ---
        {
            "name": "Muktangan Bugdi",
            "category": "bugadi",
            "price": 499,
            "material": "Basra Pearl · Red & Green Bead Drops",
            "description": "Delicate classic Maharashtrian pearl bugdi with dangling colorful beads.",
            "stock": "IN STOCK",
            "image": "static/images/bugadi/MuktanganBugdi.png"
        },
        {
            "name": "Mastya Bugdi ",
            "category": "bugadi",
            "price": 699,
            "material": "Red Meenakari · Pearl Border & Chain Drops",
            "description": "Unique fish motif traditional bugdi styled as an upper ear earcuff.",
            "stock": "IN STOCK",
            "image": "/static/images/bugadi/MastyaBugdi.png"
        },
        {
            "name": "Traditional Bugdi",
            "category": "bugadi",
            "price": 549,
            "material": "Red Gemstone · Kundan Work & Pearls",
            "description": "Classic Maharashtrian press bugdi featuring ruby stone center and pearl drops.",
            "stock": "IN STOCK",
            "image": "static/images/bugadi/TraditionalBugdi.png"
        },
        {
            "name": "Pachi Kundan Bugdi",
            "category": "bugadi",
            "price": 599,
            "material": "Pachi Kundan · Red & Green Enamel with Ghungroo Drops",
            "description": "Ornate semi-circular Pachi Kundan bugdi with tiny golden ghungroo clusters.",
            "stock": "IN STOCK",
            "image": "static/images/bugadi/PachiKundanBugdi.png"
        },
        # --- EARCUFF COLLECTION ---
        {
            "name": "Lavanya Side Earcuff",
            "category": "earcuff",
            "price": 599,
            "material": "Ruby Red Stones · Gold Plated Bead Edges & Seed Pearls",
            "description": "Charming side earcuff with bright ruby stones and pearl trim.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/LavanyaSideEarcuff.png"
        },
        {
            "name": "AD Stone Side Earcuff",
            "category": "earcuff",
            "price": 599,
            "material": "Green Emerald Center · AD/Kundan Petal Stones & Pearl Accents",
            "description": "Sparkling AD stone side earcuff crafted to pair seamlessly with any saree.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/ADStoneSideEarcuff.png"
        },
        {
            "name": "Fish Earcuff (Green Meenakari)",
            "category": "earcuff",
            "price": 699,
            "material": "Green & Red Enamel · Gold Bead Wire Frame",
            "description": "Eye-catching fish-shaped ear wrap cuff in rich green and red meenakari.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/FishEarcuff.png"
        },
        {
            "name": "Pearl Earcuff Set",
            "category": "earcuff",
            "price": 800,
            "material": "Handcrafted Seed Pearls · Floral Ruby & Emerald Accents · Golden Jhumka Drops",
            "description": "Exquisite artisanal pearl ear cuff set featuring intricate floral stone clusters and dangling textured jhumkis.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/PearlEarcuffSet.png"
        },
        {
            "name": "Nathicha Saaj Grand Earcuff",
            "category": "earcuff",
            "price": 850,
            "material": "Sunburst Gold Wire Fringe · Pearl Rosettes · Filigree Jhumkis",
            "description": "Statement bridal ear cuff featuring radiating gold spike details, multi-color stone centers, and full jhumka drops.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/NathichaSaajGrandEarcuff.png"
        },
        {
            "name": "Moti Nath Karnsaj",
            "category": "earcuff",
            "price": 700,
            "material": "Basra Pearls · Red Teardrop Gemstone & Gold Beads",
            "description": "Graceful ear-hugging pearl motif earcuffs styled like a traditional nath.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/MotiNathKarnsaj.png"
        },
        {
            "name": "Kanvel (Multi-Layer Ear Chains)",
            "category": "earcuff",
            "price": 499,
            "material": "Hand-strung Pearls · Rice-Pearl Leaf Fringe",
            "description": "Multi-tier beaded ear chains with dangling rice pearl tassels.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/Kanvel.png"
        },
        {
            "name": "Parijatak Jhumka",
            "category": "earcuff",
            "price": 200,
            "material": "Petal Shaped Pearls · Ruby Red Center Stone & Golden Jhumka Drop",
            "description": "Handcrafted floral parijat pearl studs with delicate gold bell jhumkis.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/ParijatakJhumka.png"
        },
        {
            "name": "Double Flower Jhumka",
            "category": "earcuff",
            "price": 399,
            "material": "Stacked Pearl Flowers · Ruby Stones & Pearl Bead Trim",
            "description": "Statement double-tiered floral pearl jhumkis with ruby centers.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/DoubleFlowerJhumka.png"
        },
        {
            "name": "Parijatak Kanvel",
            "category": "earcuff",
            "price": 699,
            "material": "Parijat Flower Studs · Gold Jhumki Drops & Pearl Strand Extensions",
            "description": "Complete traditional parijat jhumki set with triple-layer hair/ear chain attachments.",
            "stock": "IN STOCK",
            "image": "static/images/earcuff/ParijatakKanvel.png"
        },
        # --- HAIR ACCESSORIES COLLECTION ---
        {
            "name": "Hair Brooch",
            "category": "hair accessories",
            "price": 700,
            "material": "Pink Enamel Chandrakor · Hand-Strung Pearl Tassels",
            "description": "Traditional crescent hair brooch with multiple cascading pearl chains.",
            "stock": "IN STOCK",
            "image": "static/images/hair accessories/Hair Brooch.png"
        },
        {
            "name": "Peacock Bridal Hair Accessory",
            "category": "hair accessories",
            "price": 699,
            "material": "Twin Peacock Meenakari · Kundan Stones & Emerald Pearl Chains",
            "description": "Bridal hair ornament featuring twin peacock motifs with green bead hangings.",
            "stock": "IN STOCK",
            "image": "static/images/hair accessories/PeacockBridalHairAccessory.png"
        },

        # --- RINGS COLLECTION ---
        {
            "name": "Exclusive Royal Rings",
            "category": "ring",
            "price": 499,
            "material": "Adjustable Gold Plated Band · Ghungroo & Lotus/Crescent Enamel Motifs",
            "description": "Traditional Maharashtrian adjustable statement rings with crescent, lotus, and ghungroo details.",
            "stock": "IN STOCK",
            "image": "static/images/ring/ExclusiveRoyalRings.png"
        },
        {
            "name": "Parijatak Ring",
            "category": "ring",
            "price": 299,
            "material": "Double-Tier Woven Rice Pearls · Center Emerald Green Gemstone",
            "description": "Double-layered parijat flower statement ring featuring an emerald green centerpiece.",
            "stock": "IN STOCK",
            "image": "static/images/ring/ParijatakRing.png"
        },
        # --- ANKLETS COLLECTION ---
        {
            "name": "Moti Jul Anklet",
            "category": "anklet",
            "price": 399,
            "material": "Double Pearl Layer · Red Floral Gem Drop · Pearl Tassels",
            "description": "Handmade double-strand delicate pearl anklet featuring a red floral cluster center with dangling seed pearls.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/MotiJulAnklet.png"
        },
        {
            "name": "Kundan Layered Anklet",
            "category": "anklet",
            "price": 499,
            "material": "Gold Chain & Pearl Layer · Kundan Floral Pendant · Pearl Clusters",
            "description": "Dual-layer anklet combining fine gold link chain and pearl strand with a Kundan stone center drop.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/KundanLayeredAnklet.png"
        },
        {
            "name": "Green Moti Jul Anklet",
            "category": "anklet",
            "price": 499,
            "material": "Double Pearl Strand · Emerald Green Lotus Center Stone · Kundan Trim",
            "description": "Vibrant emerald green stone central charm framed by double pearl strands and Kundan accents.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/GreenMotiJulAnklet.png"
        },
        {
            "name": "Kamal Ghungroo Anklet",
            "category": "anklet",
            "price": 599,
            "material": "Gold Bead Chain · Red Meenakari Lotus Motif · Golden Ghungroo Drops",
            "description": "Traditional gold beaded anklet highlighting red lotus motifs with dangling golden bells.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/KamalGhungrooAnklet.png"
        },
        {
            "name": "Lotus Anklet",
            "category": "anklet",
            "price": 499,
            "material": "Gold Chain · Pink Gem Lotus Motifs · Ruby Drop Beads",
            "description": "Delicate chain anklet adorned with repeating ruby-pink lotus motifs and bead drops.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/LotusAnklet.png"
        },
        {
            "name": "Exclusive Parrot Anklet",
            "category": "anklet",
            "price": 449,
            "material": "Sleek Gold Link Chain · Enamel Parrot Motif · Pearl Accents",
            "description": "Charming traditional parrot-shaped center charm on a delicate gold link chain.",
            "stock": "IN STOCK",
            "image": "static/images/anklet/ExclusiveParrotAnklet.png"
        }
    ]

    products_collection.insert_many(all_products)

@app.route('/')
def home():
    return render_template('index.html', categories=CATEGORIES)

@app.route('/admin')
def admin():
    return render_template('admin.html', categories=[c for c in CATEGORIES if c != 'all'])

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products():
    if request.method == 'POST':
        data = request.json
        new_product = {
            "name": data.get("name"),
            "category": data.get("category"),
            "price": int(data.get("price", 0)),
            "material": data.get("material", "22K Gold Plated"),
            "description": data.get("description", ""),
            "stock": data.get("stock", "IN STOCK"),
            "image": data.get("image")
        }
        result = products_collection.insert_one(new_product)
        return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

    category = request.args.get('category', 'all')
    search = request.args.get('search', '').strip().lower()
    
    query = {}
    if category != 'all':
        query['category'] = category
    if search:
        query['name'] = {'$regex': search, '$options': 'i'}

    products = list(products_collection.find(query))
    for p in products:
        p['_id'] = str(p['_id'])
        
    return jsonify(products)

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        products_collection.delete_one({"_id": ObjectId(product_id)})
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    force_reset_and_seed()  # Resets database automatically on start
    app.run(debug=True, port=5000)