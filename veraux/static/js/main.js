/**
 * Veraux Main Scripts
 * Handles global UI interactions like navigation, cart count updates.
 */

import { cart } from './cart.js';

document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();

    // Subscribe to cart changes to update header count globally
    cart.subscribe(() => {
        updateCartCount();
    });

    // Mobile Menu Toggle (To be implemented once HTML structure exists)
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            const isOpen = navMenu.classList.contains('active');
            mobileMenuBtn.setAttribute('aria-expanded', isOpen);
        });
    }

    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

function updateCartCount() {
    const countElements = document.querySelectorAll('.cart-count');
    const count = cart.getCount();

    countElements.forEach(el => {
        el.textContent = count;
        el.style.display = count > 0 ? 'inline-flex' : 'none';
    });
}
