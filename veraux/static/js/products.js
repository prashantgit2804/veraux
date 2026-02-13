/**
 * Veraux Product Data
 * Designed for scalability: Supports multiple categories (Jewelry, Watches, Perfumes, etc.)
 */

export const products = [
    // Jewelry Collection
    {
        id: "j-001",
        name: "Ethereal Diamond Necklace",
        category: "jewelry",
        subCategory: "necklaces",
        price: 1250.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1599643478518-17488fbbcd75?q=80&w=1000&auto=format&fit=crop",
        description: "A stunning masterpiece featuring a solitaire diamond on a delicate 18k gold chain.",
        material: "18k Gold, Diamond",
        isBestseller: true,
        isNew: false
    },
    {
        id: "j-002",
        name: "Obsidian Gold Ring",
        category: "jewelry",
        subCategory: "rings",
        price: 850.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1626784215021-2e39ccf971cd?q=80&w=1000&auto=format&fit=crop",
        description: "Modern minimalist design meeting timeless luxury. Perfect for everyday elegance.",
        material: "24k Gold Plated",
        isBestseller: true,
        isNew: true
    },
    {
        id: "j-003",
        name: "Sapphire Drop Earrings",
        category: "jewelry",
        subCategory: "earrings",
        price: 950.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=1000&auto=format&fit=crop",
        description: "Elegant drop earrings featuring deep blue sapphires encrusted in silver.",
        material: "Silver, Sapphire",
        isBestseller: false,
        isNew: true
    },
    {
        id: "j-004",
        name: "Rose Gold Bracelet",
        category: "jewelry",
        subCategory: "bracelets",
        price: 450.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=1000&auto=format&fit=crop",
        description: "Subtle and chic, this rose gold bracelet adds a touch of warmth to any outfit.",
        material: "14k Rose Gold",
        isBestseller: true,
        isNew: false
    },
    
    // Future Categories (Scalabiity Test)
    {
        id: "w-001",
        name: "Veraux Chrono Royal",
        category: "watches",
        price: 3200.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?q=80&w=1000&auto=format&fit=crop",
        description: "Swiss movement, sapphire crystal glass, and Italian leather strap.",
        material: "Stainless Steel, Leather",
        isBestseller: false,
        isNew: true
    },
    {
        id: "p-001",
        name: "Midnight Essence",
        category: "perfumes",
        price: 180.00,
        currency: "USD",
        image: "https://images.unsplash.com/photo-1594035910387-fea4779426e9?q=80&w=1000&auto=format&fit=crop",
        description: "A deep, woody fragrance with top notes of bergamot and base notes of oud.",
        material: "Eau de Parfum",
        isBestseller: false,
        isNew: true
    }
];
