# Kalakruti | Handcrafted Maharashtrian Jewellery

 Kalakruti is a full-stack e-commerce web platform dedicated to showcasing and selling authentic Maharashtrian heritage jewellery (such as Thushi, Nath, and traditional necklaces). Built with Python Flask and Bootstrap 5.

---

##  Demo & Screen Recording

Here is a live walkthrough of the Kalakruti web application in action:

<video src="https://github.com/user-attachments/assets/0b056be2-bc0a-456a-9a4c-2d9340a5a38d" controls width="100%"></video>

---

##  Application Screenshots

### Homepage & Product Catalogue
| :---: |

<p align="left">
  <img src="assets/HomePage.png" alt="Homepage" width="80%">
</p>

### Features Overview
| Product Quick View Modal | Interactive Cart Drawer |
| :---: | :---: |
| ![Product Quick View](assets/modal.png) | ![Cart Drawer](assets/cart.png) |

| User Account & Sign-In |
| :---: |
| ![User Profile](assets/profile.png) |

---

##  Key Features

* **Dynamic Product Catalogue**: Browse items filtered instantly by traditional categories (Thushi, Nath, etc.).
* **Instant Search Bar**: Dynamic filtering of products by keyword.
* **Interactive Cart Drawer**: Real-time total calculation, item tracking, and clear-cart functionalities.
* **Product Quick View**: Pop-up modal displaying product specifications, materials, pricing, and availability.
* **User Session & Profile Management**: Offcanvas drawer tracking signed-in users and their active order status.
* **Responsive UI**: Styled using custom CSS, Jinja2 templating, and Bootstrap 5.

---

## 🛠️ Tech Stack & Languages

### Languages
* **Python**: Backend server logic & routing
* **HTML5**: Page structure & semantic components
* **CSS3**: Custom styling, Flexbox layouts & custom tokens
* **JavaScript (ES6+)**: DOM manipulation, cart management, and modal handling

### Frameworks & Libraries
* **Flask**: Web framework
* **Jinja2**: HTML templating engine
* **Bootstrap 5**: UI components & grid system
* **Bootstrap Icons**: Vector icons

---

## 📁 Project Structure

```text
NGD_PROJECT/
├── app.py                  # Main Flask application entry point
├── requirements.txt        # Python dependencies
├── assets/                 # Readme screenshots & demo GIF
│   ├── demo.gif
│   ├── homepage.png
│   ├── modal.png
│   ├── cart.png
│   └── profile.png
├── static/                 # CSS, JS, and product images
│   ├── css/
│   └── js/
└── templates/              # HTML templates (index.html, etc.)


## Getting Started

### Prerequisites
* Python 3.10+
* Git

### Local Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/rupalijadhav-rgb/Jwellery_Project.git
   cd Jwellery_Project
    ```

2. **Activate Virtual Environment**
    ```powerShell
    .\venv\Scripts\Activate.ps1
    ```

    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**
    ```bash
    python app.py
    ```
    Open http://127.0.0.1:5000/ in your browser.
    

## Author

* **Developer**: Rupali Jadhav
* **GitHub**: [@rupalijadhav-rgb](https://github.com/rupalijadhav-rgb)
* **Repository**: [Jwellery_Project](https://github.com/rupalijadhav-rgb/Jwellery_Project)
