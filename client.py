import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/books"

# Client runner.
def run_client():
    print(f"Fetching books from FastAPI endpoint: {API_URL}")
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FastAPI microservice: {e}")
        return

    books_data = response.json()
    print(f"Successfully fetched {len(books_data)} book records.")

    # Load into Pandas DataFrame
    df = pd.DataFrame(books_data)

    # Print DataFrame to console
    print("\n--- Extracted Book Data (Pandas DataFrame) ---")
    print(df.to_string(index=False))

    # Export DataFrame to CSV
    csv_filename = "exported_books.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nSaved DataFrame to '{csv_filename}'")

    # Generate scatter plot chart
    generate_scatter_plot(df)

# Generate scatter plot of price vs rating
def generate_scatter_plot(df: pd.DataFrame):
    plt.figure(figsize=(9, 6))

    # Plot points
    plt.scatter(
        df['price'],
        df['rating'],
        color='#2b5c8f',
        alpha=0.75,
        s=100,
        edgecolors='black',
        linewidth=1
    )

    # Set labels and title
    plt.title("Book Price vs. Star Rating", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Price (£)", fontsize=12, labelpad=10)
    plt.ylabel("Rating (1-5 Stars)", fontsize=12, labelpad=10)

    # Set ticks and grid
    plt.yticks([1, 2, 3, 4, 5])
    plt.grid(True, linestyle='--', alpha=0.5)

    # Annotate short titles on plot points
    for _, row in df.iterrows():
        short_title = row['title'][:15] + "..." if len(row['title']) > 15 else row['title']
        plt.annotate(
            short_title,
            (row['price'], row['rating']),
            textcoords="offset points",
            xytext=(0, 7),
            ha='center',
            fontsize=8,
            alpha=0.8
        )

    plt.tight_layout()

    # Save chart image
    output_img = "price_vs_rating.png"
    plt.savefig(output_img, dpi=300)
    plt.close()
    print(f"Scatter plot successfully generated and saved to '{output_img}'!")

if __name__ == "__main__":
    run_client()
