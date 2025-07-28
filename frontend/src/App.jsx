import React, { useState } from "react";

const ALLERGIES = [
  "milk",
  "eggs",
  "fish",
  "crustacean shellfish",
  "tree nuts",
  "peanuts",
  "wheat",
  "soybeans",
  "sesame",
];

function App() {
  const [image, setImage] = useState(null);
  const [allergies, setAllergies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setResults(null);
    setError("");
  };

  // Preview image URL
  const imagePreviewUrl = image ? URL.createObjectURL(image) : null;

  const handleAllergyChange = (e) => {
    const value = Array.from(
      e.target.selectedOptions,
      (option) => option.value
    );
    setAllergies(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);
    setError("");
    const formData = new FormData();
    formData.append("image", image);
    allergies.forEach((a) => formData.append("allergies", a));
    try {
      const res = await fetch("http://localhost:8000/detect-food", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setResults(data);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Network error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="app-title">Taste Buds</div>
      {!results && (
        <form className="upload-section" onSubmit={handleSubmit}>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            required
          />
          {imagePreviewUrl && (
            <div style={{
              border: "2px solid #6366f1",
              borderRadius: "12px",
              marginBottom: "1rem",
              width: "220px",
              height: "220px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "#f3f4f6"
            }}>
              <img
                src={imagePreviewUrl}
                alt="Preview"
                style={{
                  maxWidth: "200px",
                  maxHeight: "200px",
                  borderRadius: "8px",
                  objectFit: "contain"
                }}
              />
            </div>
          )}
          <label htmlFor="allergies">Allergies:</label>
          <select
            id="allergies"
            multiple
            value={allergies}
            onChange={handleAllergyChange}
            style={{ marginBottom: "1rem", minWidth: "200px" }}
          >
            {ALLERGIES.map((a) => (
              <option key={a} value={a}>
                {a.charAt(0).toUpperCase() + a.slice(1)}
              </option>
            ))}
          </select>
          <button type="submit" disabled={loading || !image}>
            Detect Food & Get Recipes
          </button>
        </form>
      )}
      {loading && (
        <div className="loading">
          <div className="loader"></div>
          <div>Analyzing your photo...</div>
        </div>
      )}
      {error && (
        <div className="results" style={{ color: "#ef4444" }}>{error}</div>
      )}
      {results && (
        <div className="results" style={{ minHeight: "80vh" }}>
          <div className="recipe-list">
            <h2>Recommended Recipes</h2>
            {results.recipes && results.recipes.length > 0 ? (
              results.recipes.map((recipe, idx) => (
                <div className="recipe" key={idx}>
                  <div className="recipe-title">{recipe.title}</div>
                  <div>
                    <strong>Ingredients:</strong>
                    <ul className="ingredient-list">
                      {recipe.ingredients.map((ing, i) => (
                        <li key={i}>{ing}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="instructions">
                    <strong>Instructions:</strong> {recipe.instructions}
                  </div>
                </div>
              ))
            ) : (
              <div>No recipes found.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
