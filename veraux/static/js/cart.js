/**
 * Veraux Cart Management
 * Handles adding, removing, updates, and persistence.
 */

export class Cart {
    constructor() {
        this.key = 'veraux_cart';
        this.items = this.load();
        this.listeners = [];
    }

    load() {
        const stored = localStorage.getItem(this.key);
        return stored ? JSON.parse(stored) : [];
    }

    save() {
        localStorage.setItem(this.key, JSON.stringify(this.items));
        this.notify();
    }

    add(product, quantity = 1) {
        const existing = this.items.find(item => item.id === product.id);
        if (existing) {
            existing.quantity += quantity;
        } else {
            this.items.push({ ...product, quantity });
        }
        this.save();
        alert(`${product.name} added to cart.`); // Simple feedback for now
    }

    remove(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
    }

    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = parseInt(quantity);
            if (item.quantity <= 0) this.remove(productId);
            else this.save();
        }
    }

    clear() {
        this.items = [];
        this.save();
    }

    getCount() {
        return this.items.reduce((total, item) => total + item.quantity, 0);
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    // Simple observer pattern to update UI when cart changes
    subscribe(callback) {
        this.listeners.push(callback);
    }

    notify() {
        this.listeners.forEach(cb => cb(this.items));
    }
}

export const cart = new Cart();
