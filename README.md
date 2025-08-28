# Please credit Mohammad Ahsan Hummayoun when using, sharing, or adapting this code

Tour operators of the Dubai Desert Safari are unable to notify tourists about potential delays in the advertised pickup times. This workflow is designed to handle that communication via Whatsapp. Using a free route selection API, it calculates the estimated pickup time and based on an algorithm, it sends a confirmation/delay message.

This solution can be applied to any tour or service business that relies on timely pickups, providing a reliable way to manage customer expectations.

To run, you need to set up a .env file with your API credentials. You'll also need to have two CSV files: 

bookings.csv and drivers.csv.

This workflow relies on external APIs:

OpenRouteService (ORS_API_KEY) for geocoding and calculating ETAs.

Twilio Sandbox (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM) for sending the WhatsApp messages.


