# Fitness Tracker Project

## Overview
The **Fitness Tracker** project is a Django-based web application that helps users monitor their fitness activities, meals, and sleep logs while providing personalized insights and statistics. The project utilizes RESTful APIs, Celery for asynchronous tasks, caching for performance optimization, and advanced database queries for data aggregation and analytics.

The system also features Swagger integration for API documentation, ensuring a seamless developer experience.

---

## Features
### Key Functionalities:
1. **User Management:**
   - API endpoints for user authentication and management under `/api/user/`.

2. **Wellness Tracking:**
   - Users can log fitness activities, meals, and sleep data through `/api/wellness/`.
   - **Fitness Activities:**
     - Users can log details such as the type of activity (e.g., running, cycling, swimming), the duration in minutes, and calories burned.
     - Calories burned are calculated using the [CalorieNinjas CaloriesBurned API](https://calorieninjas.com/api/caloriesburned), providing accurate estimations for different activity types and durations.
   - **Meals:**
     - Users can log meals with descriptions and the number of calories consumed.
     - Calorie information is retrieved via the [CalorieNinjas API](https://calorieninjas.com/api/).
   - **Sleep Logs:**
     - Users can record the number of hours slept, the quality of sleep (e.g., poor, moderate, good), bedtime, and wakeup time.
     - This information helps track sleep patterns and their impact on overall wellness.

3. **Insights Generation:**
   - Insights on fitness, meals, and sleep data are accessible via `/api/insights/`.
   - Includes daily, weekly, and monthly statistics on:
     - Average calories burned per day.
     - Average calories consumed per day.
     - Average sleep hours per day.
     - Most common activity types.

4. **API Documentation:**
   - Interactive Swagger UI is available at `/swagger/` for developers to explore the API endpoints.

---

## Technical Highlights
### APIs for Calorie Calculations
- **External APIs:** Calories burned during activities are calculated by integrating external APIs. Cached results minimize redundant calls for the same activity types and durations.
- **Custom Throttling:** Throttling is implemented on daily, weekly, and monthly insight endpoints to limit user requests (e.g., daily report accessible only once per day).

### Celery with Redis
- **Asynchronous Insight Generation:** Celery is used to offload the computationally heavy task of generating insights to background workers, ensuring the API remains responsive.
- **Weekly Email Notifications:** Celery sends weekly email summaries of insights to subscribed users.
- **Redis:** Serves as the message broker for Celery, enabling task queuing and monitoring.

### Caching
- **Performance Optimization:**
  - Calories for common activities are cached in Redis to reduce API calls.
  - Cached results are updated periodically or when significant changes occur.

### Database Queries
- **Django ORM:**
  - Complex queries using `annotate`, `aggregate`, and `annotate` are used to compute insights directly from the database, reducing the need for additional processing.
- **Examples:**
  - Daily average calories burned: `Sum('calories') / Count('date', distinct=True)`.
  - Most common activity type: `values('activity_type').annotate(count=Count('activity_type')).order_by('-count')`.

---

## Implementation Details

### URL Structure
- **Admin Panel:** `/admin/`
- **User APIs:** `/api/user/`
- **Wellness APIs:** `/api/wellness/`
- **Insights APIs:** `/api/insights/`
- **Swagger Documentation:** `/swagger/`

### Insights Generation Workflow
1. **User Data Logging:** Users log fitness, meal, and sleep data through wellness APIs.
2. **Task Offloading:**
   - A Celery task is triggered to process insights asynchronously.
   - The task uses complex database queries for summarizing user data.
3. **Caching:** Frequently requested data (e.g., calorie calculations) is cached.
4. **Insight Retrieval:** Users retrieve insights via `/api/insights/`, which uses cached data where available.

### Daily, Weekly, Monthly Insights
- **Throttling:** Custom throttling limits users to one request per period (e.g., daily).
- **Statistics Calculation:**
  - Average calories burned and consumed.
  - Average sleep duration.
  - Most frequent activities and sleep quality.

---

## Technology Stack
### Backend
- **Django**: Main web framework for application logic and APIs.
- **Django REST Framework (DRF)**: API development and custom throttling.

### Asynchronous Task Processing
- **Celery**: Background job queue for generating insights and sending emails.
- **Redis**: Message broker and cache.

### Other Integrations
- **Swagger (drf-spectacular)**: Interactive API documentation.

---

## Installation

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/username/fitness-tracker.git
   cd fitness-tracker
   ```
2. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Configure `.env` with the required API keys 

4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Start Redis:
   ```bash
   redis-server
   ```
6. Start Celery:
   ```bash
   celery -A fitness_tracker worker --loglevel=info
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## Future Enhancements
- Add gamification elements like badges and streaks.
- Provide advanced analytics using machine learning for activity predictions.
- Expand API integrations for fitness wearables.

---

## Contact
For issues or feature requests, open an issue on the [GitHub repository](https://github.com/username/fitness-tracker).

