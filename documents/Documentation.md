# **URL-Shortner 🔗**

## **About Our Project**

About Our URL-Shortner Project

The URL-Shortner project is a powerful tool built to transform lengthy, complex URLs into concise, easy-to-share links, perfect for social media, marketing campaigns, and much more. With real-time analytics and click-tracking, our URL-Shortner offers a seamless experience for users who value efficiency and insight.

Why the unique spelling? Because URL-Shortner is all about making things short, simple, and quick to share. Unlike other solutions, our tool is ad-free and straightforward, providing a hassle-free way to create, update, and manage URLs.

Why Choose URL-Shortner?

* User-Friendly Design: A clean, intuitive interface that allows you to shorten URLs, update them as needed, or delete them if they’re no longer in use—all in just a few clicks.  
* Efficient URL Management: Solve common URL issues like unwieldy links, misspellings, or frequently updated content by creating short URLs that you can easily revise or remove.  
* Built for You: Whether you're a marketer, content creator, or just someone who needs a reliable URL management tool, URL-Shortner is designed with your needs in mind.

**Intro Video:** https://drive.google.com/file/d/1jwc0y7n9G4qazXlhjZdKU3kvVnhvgEIo/view?usp=drive\_link

---

## **Key Features**

1. **Customizable URL Stubs**  
   * Personalize short URLs with custom text, creating memorable, brand-aligned links that enhance user engagement.  
2. **Comprehensive URL Analytics**  
   * Track link clicks, geographic data, and other metrics to gain valuable audience insights and optimize your campaigns.  
3. **Efficient Bulk URL Upload**  
   * Upload multiple URLs in CSV format, ideal for managing large volumes of links quickly and efficiently.  
4. **Secure and Reliable Management**  
   * Encrypted URL management ensures your links and data are secure, letting you focus on growing your brand.  
5. **Multiple Formats for Bulk Uploads**  
   * Add URLs and stubs using a CSV or as a comma-separated list for flexibility.

---

## **User Testimonials**

* *"The URL shortener has been a game-changer for my marketing campaigns\!"* — **Smeet Nagda**  
* *"The bulk upload feature saves me hours every week."* — **Jason Perez**  
* *"Detailed analytics have helped me understand my audience's engagement."* — **Devansh Shah**  
* *"Encrypted URL management gives me peace of mind."* — **Gaurav Mehta**  
* *"The ability to create branded URLs has been a total productivity booster\!"* — **Yash Shah**

---

## **Getting Started**

## **How to Use**

**1\. Generate a Short URL**

* Visit yoururl.tech/url-shortner.  
* Enter the long URL and click **Get short URL** to receive a popup displaying the shortened URL and an access code. Save this access code for future updates or deletions, as it won’t be accessible later.

**2\. Bulk URL Upload**

* To manage multiple URLs at once, you have two options:  
  * **CSV Upload**: Upload a CSV file containing the long URLs you want to shorten, and the system will process each URL and generate short links.  
  * **Comma-Separated Text**: Enter multiple URLs in the text field separated by commas, and the shortener will process each URL.

**3\. Update an Existing URL**

* Click on **Update Existing URL** and enter the following:  
  * **Short URL stub**: This is the last part of your short URL (e.g., in `http://yoururl.tech/oe7p1SKtPS`, `oe7p1SKtPS` is the stub).  
  * **Access Code**: Use the code given at the time of creation.  
  * **Updated Long URL**: Enter the new destination URL.  
* Click **Update URL**, and if validated, your URL will be updated.

**4\. Delete a URL**

* To delete an existing URL, click **Delete Existing URL** and enter the access code. You can also delete all URLs at once from the table if needed.

**5\. Export Statistics**

* You can export link statistics at any time to save them locally. This feature allows you to back up valuable insights and use the data for further analysis.

---

## **Development and Deployment**

The URL-Shortner’s backend is built in **Django** while the front end uses **Angular**. It is deployed via **PythonAnywhere**.

### **Development**

To contribute, follow these steps:

1. Clone the repository.  
2. Install Python 3\.  
3. Run `pip install -r requirements.txt`.  
4. Start the server with `python manage.py runserver`.  
5. Visit `http://localhost:8000/admin` to access the Django admin interface.

### **Deployment**

Follow deployment instructions here.

---

## **Troubleshooting**

| Status Code | Description | Resolution |
| ----- | ----- | ----- |
| 400 | Bad Request | Verify the HTTP request format. |
| 404 | Not Found | Check the URL or endpoint validity. |
| 405 | Method Not Allowed | Ensure the correct HTTP method is used. |
| 500 | Internal Server Error | Check server logs for unhandled exceptions. |

---

## **File Descriptions**

* **manage.py**: For running Django commands.  
* **db.sqlite3**: Project database (not included in the repo; generated on setup).  
* **requirements.txt**: Lists dependencies for the project.

### **Exporting Data**

Use `python manage.py dumpdata > data.json` to export project data in JSON format.

---

## **API Documentation**

Our **Django API** (in the `url_shortner_server` project) is designed to handle URL shortening tasks, housed under the `shortner` app.

Sub-modules:

* **shortner.admin**: Admin functionalities.  
* **shortner.apps**: Application configuration.  
* **shortner.constants**: Stores application constants.  
* **shortner.delete\_view**: Defines the delete view.  
* **shortner.models**: Manages data models.  
* **shortner.new\_view**: Defines the NewView view.  
* **shortner.stub\_view**: Handles stub views.  
* **shortner.update\_view**: Defines the UpdateView view.  
* **shortner.tests**: Contains test cases.  
* **shortner.views**: Core view functions for the application.

---

## **Adding Test Cases**

How to add tests for this repo?  
in the folder shortner refer to tests folder.  
file test\_views tests the different view handler for the application  
file test\_models tests different models by checking whether the database calls are working  
file test\_urls test whether the right handlers are called for a view.

---

**Badges and Integrations**

* GitHub Release  
* GitHub Tag  
* GitHub Forks  
* GitHub Stars  
* GitHub Issues  
* CodeCov  
* ESLint  
* Build & Push WebApp  
* CodeQL  
* Test & Coverage

Contributors

Akshat Shah  
Prerak Bhandari  
Dhairya Shah  
Made by Teams 5, 16, 21
