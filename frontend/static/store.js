const API_URL = "/api/v1/books";

let allBooks = [];
let cart = [];

// Load cart data saved in the browser
const savedCart = localStorage.getItem("bookstore_cart");

if (savedCart) {
    cart = JSON.parse(savedCart);
}

// Save cart data in the browser
function saveCart() {
    localStorage.setItem("bookstore_cart", JSON.stringify(cart));
}

// Run after the page loads
document.addEventListener("DOMContentLoaded", () => {

    // Catalogue elements
    const booksGrid = document.getElementById("books-grid");
    const searchInput = document.getElementById("book-search");
    const categoryFilter = document.getElementById("category-filter");

    // Book details popup
    const bookModal = document.getElementById("book-modal");
    const closeBookModal = document.getElementById("close-modal");

    // Cart elements
    const cartButton = document.getElementById("cart-button");
    const cartModal = document.getElementById("cart-modal");
    const closeCart = document.getElementById("close-cart");
    const cartItems = document.getElementById("cart-items");
    const cartCount = document.getElementById("cart-count");
    const cartTotal = document.getElementById("cart-total");


    // Load books from FastAPI
    async function loadBooks() {

        try {
            booksGrid.innerHTML = "<p>Loading books...</p>";

            const response = await fetch(API_URL);

            if (!response.ok) {
                throw new Error("Unable to load books.");
            }

            allBooks = await response.json();

            loadCategories();
            displayBooks(allBooks);

        } catch (error) {
            console.error(error);
            booksGrid.innerHTML =
                "<p>Unable to load books. Please try again.</p>";
        }
    }


    // Load book categories into dropdown
    function loadCategories() {

        const categories = [
            ...new Set(allBooks.map(book => book.category))
        ];

        categoryFilter.innerHTML =
            '<option value="all">All Categories</option>';

        categories.forEach(category => {

            const option = document.createElement("option");

            option.value = category;
            option.textContent = category;

            categoryFilter.appendChild(option);
        });
    }


    // Display book cards
    function displayBooks(books) {

        booksGrid.innerHTML = "";

        if (books.length === 0) {
            booksGrid.innerHTML =
                "<p>No books found.</p>";
            return;
        }

        books.forEach(book => {

            const card = document.createElement("div");
            card.className = "book-card";

            const cover = document.createElement("div");
            cover.className = "book-cover";
            cover.textContent = book.title;

            const info = document.createElement("div");
            info.className = "book-info";

            const category = document.createElement("span");
            category.className = "book-category";
            category.textContent = book.category;

            const title = document.createElement("h3");
            title.textContent = book.title;

            const author = document.createElement("p");
            author.textContent = "By " + book.author;

            const price = document.createElement("p");
            price.className = "book-price";
            price.textContent = "₹" + Number(book.price).toFixed(2);

            const stock = document.createElement("p");
            stock.className = "book-stock";
            stock.textContent = "Available: " + book.stock;

            // Add to Cart button
            const addButton = document.createElement("button");
            addButton.className = "add-to-cart";
            addButton.textContent =
                book.stock > 0 ? "Add to Cart" : "Out of Stock";

            addButton.disabled = book.stock <= 0;

            addButton.addEventListener("click", event => {
                event.stopPropagation();
                addToCart(book);
            });

            info.append(
                category,
                title,
                author,
                price,
                stock,
                addButton
            );

            card.append(cover, info);

            // Open book details
            card.addEventListener("click", () => {
                openBookDetails(book);
            });

            booksGrid.appendChild(card);
        });
    }


    // Open book details popup
    function openBookDetails(book) {

        document.getElementById("modal-category").textContent =
            book.category;

        document.getElementById("modal-title").textContent =
            book.title;

        document.getElementById("modal-author").textContent =
            "By " + book.author;

        document.getElementById("modal-price").textContent =
            "₹" + Number(book.price).toFixed(2);

        document.getElementById("modal-stock").textContent =
            "Available stock: " + book.stock;

        document.getElementById("modal-description").textContent =
            book.description || "No description available.";

        bookModal.classList.add("active");
    }


    // Close book details popup
    closeBookModal.addEventListener("click", () => {
        bookModal.classList.remove("active");
    });

    bookModal.addEventListener("click", event => {
        if (event.target === bookModal) {
            bookModal.classList.remove("active");
        }
    });


    // Add book to cart
    function addToCart(book) {

        const existingItem = cart.find(
            item => item.id === book.id
        );

        const currentQuantity = existingItem
            ? existingItem.quantity
            : 0;

        if (currentQuantity >= book.stock) {
            alert("You cannot add more than the available stock.");
            return;
        }

        if (existingItem) {
            existingItem.quantity++;
        } else {
            cart.push({
                id: book.id,
                title: book.title,
                price: Number(book.price),
                stock: book.stock,
                quantity: 1
            });
        }

        saveCart();
        renderCart();

           alert(book.title + " added to your cart!");
    }


    // Display cart items
    function renderCart() {

        cartItems.innerHTML = "";

        if (cart.length === 0) {

            cartItems.textContent = "Your cart is empty.";

        } else {

            cart.forEach(item => {

                const row = document.createElement("div");
                row.className = "cart-item";

                const details = document.createElement("div");

                const title = document.createElement("strong");
                title.textContent = item.title;
                // Quantity controls
                const quantityControls = document.createElement("div");
                quantityControls.className = "quantity-controls";

                const decreaseButton = document.createElement("button");
                decreaseButton.textContent = "-";

                const quantityText = document.createElement("span");
                quantityText.textContent = item.quantity;

                const increaseButton = document.createElement("button");
                increaseButton.textContent = "+";

                // Decrease quantity
                decreaseButton.addEventListener("click", () => {
                    changeQuantity(item.id, -1);
                });

                // Increase quantity
                increaseButton.addEventListener("click", () => {
                    changeQuantity(item.id, 1);
                });

                quantityControls.append(
                    decreaseButton,
                    quantityText,
                    increaseButton
                );

                const price = document.createElement("p");
                price.textContent =
                    "₹" + (item.price * item.quantity).toFixed(2);

                details.append(title, quantityControls, price);
                const removeButton =
                    document.createElement("button");

                removeButton.className = "remove-cart-item";
                removeButton.textContent = "Remove";

                removeButton.addEventListener("click", () => {
                    removeFromCart(item.id);
                });

                row.append(details, removeButton);

                cartItems.appendChild(row);
            });
        }

        // Calculate total quantity
        const totalQuantity = cart.reduce(
            (total, item) => total + item.quantity,
            0
        );

        // Calculate total price
        const totalPrice = cart.reduce(
            (total, item) => total + item.price * item.quantity,
            0
        );

        cartCount.textContent = totalQuantity;
        cartTotal.textContent = totalPrice.toFixed(2);
    }

    // Change book quantity
    function changeQuantity(bookId, change) {

        const item = cart.find(book => book.id === bookId);

        if (!item) {
            return;
        }

        // Increase quantity
        if (change === 1) {

            if (item.quantity >= item.stock) {
                alert("Available stock limit reached.");
                return;
            }

            item.quantity++;
        }

        // Decrease quantity
        if (change === -1) {

            item.quantity--;

            // Remove book if quantity becomes zero
            if (item.quantity <= 0) {
                removeFromCart(bookId);
                return;
            }
        }

        saveCart();
        renderCart();
    }
    // Remove book from cart
    // Remove book from cart
    function removeFromCart(bookId) {

        cart = cart.filter(item => item.id !== bookId);

        saveCart();
        renderCart();
    }

    // Open shopping cart
    cartButton.addEventListener("click", () => {

        renderCart();

        cartModal.classList.add("active");
    });


    // Close shopping cart
    closeCart.addEventListener("click", () => {
        cartModal.classList.remove("active");
    });

    cartModal.addEventListener("click", event => {

        if (event.target === cartModal) {
            cartModal.classList.remove("active");
        }
    });


    // Search books
    function filterBooks() {

        const searchText = searchInput.value.toLowerCase().trim();
        const selectedCategory = categoryFilter.value;

        const filteredBooks = allBooks.filter(book => {

            const matchesSearch =
                book.title.toLowerCase().includes(searchText) ||
                book.author.toLowerCase().includes(searchText) ||
                book.category.toLowerCase().includes(searchText);

            const matchesCategory =
                selectedCategory === "all" ||
                book.category === selectedCategory;

            return matchesSearch && matchesCategory;
        });

        displayBooks(filteredBooks);
    }


    searchInput.addEventListener("input", filterBooks);

    categoryFilter.addEventListener("change", filterBooks);


    // Initial cart display
    renderCart();

    // Initial book loading
    loadBooks();

});
