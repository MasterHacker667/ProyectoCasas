import os

# List of required libraries
libraries = [
    "pandas",
    "numpy",
    "matplotlib",
    "scipy",
    "psycopg2-binary",
    "pymysql",
    "pymongo",
    "scikit-learn",
    "pdfkit"
]

# Install libraries using pip
for lib in libraries:
    os.system(f"pip install {lib}")

print("Libraries installed successfully!")