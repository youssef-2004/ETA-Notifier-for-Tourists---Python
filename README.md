# Please credit Mohammad Ahsan Hummayoun when using, sharing, or adapting this code

This Python workflow automates communication between tour operators and their customers by providing real-time pickup updates through WhatsApp.  
It solves the challenge of notifying customers about potential delays in advertised pickup times, ensuring smoother operations and better customer experience.

This solution is suitable for any tourism or transport business that relies on timely pickups — such as city tours, airport transfers, shuttle services, or excursion operators.

# ⚙️ How it Works

**1. Booking & Driver Data**  
The workflow reads two CSV files:  
- `bookings.csv` containing customer details and pickup locations  
- `drivers.csv` containing driver details and their current positions  

**2. Route & ETA Calculation**  
Using the **OpenRouteService API (ORS_API_KEY)**, the system calculates estimated pickup times based on driver locations, traffic, and route planning.  

**3. Delay Detection & Messaging**  
If the estimated pickup time differs from the scheduled time beyond a defined threshold, the workflow automatically determines whether to send a **confirmation** or **delay** message.  

**4. WhatsApp Notifications**  
Messages are sent to customers through the **Twilio WhatsApp Sandbox** using the credentials:  
- `TWILIO_ACCOUNT_SID`  
- `TWILIO_AUTH_TOKEN`  
- `TWILIO_WHATSAPP_FROM`  

# 🚀 Setup and Requirements

1. **Environment File**  
   Create a `.env` file containing your API credentials:  
   ```ini
   ORS_API_KEY=your_openrouteservice_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# 🚀 Setup and Requirements

1. **Environment File**  
   Create a `.env` file containing your API credentials:  
   ```ini
   ORS_API_KEY=your_openrouteservice_api_key
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

   
2. **CSV Files**
   Prepare two CSV files in the project directory:

   bookings.csv — contains customer name, phone number, pickup location, and scheduled pickup time.

   drivers.csv — contains driver ID, current location, and vehicle details.
