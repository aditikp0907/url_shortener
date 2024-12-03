module.exports = async (req, res) => {
  try {
    // Only allow POST requests
    if (req.method === 'POST') {
      const { originalUrl, companyName } = req.body;

      // Check if both original URL and company name are provided
      if (!originalUrl || !companyName) {
        return res.status(400).json({ error: "Original URL and Company Name are required." });
      }

      // Logic to generate the short URL
      const shortUrl = generateShortUrl(originalUrl, companyName);

      // Respond with the generated short URL
      res.status(200).json({ shortUrl });
    } else {
      // Handle non-POST methods (e.g., GET, PUT, etc.)
      res.status(405).json({ error: 'Method Not Allowed' });
    }
  } catch (error) {
    // Catch any unexpected errors and send a 500 status with the error message
    res.status(500).json({ error: 'Internal Server Error', details: error.message });
  }
};

// Helper function to generate the short URL
function generateShortUrl(originalUrl, companyName) {
  // Base URL for your short links
  const baseUrl = "https://short.ly/";

  // Generate a unique alias based on the company name and current timestamp
  const alias = companyName + "-" + Date.now();

  // Return the full short URL
  return baseUrl + alias;
}
