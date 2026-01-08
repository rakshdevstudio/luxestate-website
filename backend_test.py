import requests
import sys
import json
import os
from datetime import datetime

class LuxEstateAPITester:
    def __init__(self, base_url=None):
        if base_url is None:
            # Try localhost first, fallback to remote
            base_url = os.environ.get("BACKEND_URL", "http://localhost:8080")
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tokens = {}
        self.users = {}
        self.properties = {}
        self.leads = {}
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, token=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response text: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_user_registration(self):
        """Test user registration for different roles"""
        print("\n=== Testing User Registration ===")
        
        # Test client registration
        client_data = {
            "email": f"client_{datetime.now().strftime('%H%M%S')}@test.com",
            "password": "TestPass123!",
            "name": "Test Client",
            "role": "client"
        }
        success, response = self.run_test(
            "Client Registration",
            "POST",
            "auth/register",
            200,
            data=client_data
        )
        if success:
            self.tokens['client'] = response.get('token')
            self.users['client'] = response.get('user')

        # Test seller registration
        seller_data = {
            "email": f"seller_{datetime.now().strftime('%H%M%S')}@test.com",
            "password": "TestPass123!",
            "name": "Test Seller",
            "role": "seller"
        }
        success, response = self.run_test(
            "Seller Registration",
            "POST",
            "auth/register",
            200,
            data=seller_data
        )
        if success:
            self.tokens['seller'] = response.get('token')
            self.users['seller'] = response.get('user')

        # Test admin registration (should work same as others)
        admin_data = {
            "email": f"admin_{datetime.now().strftime('%H%M%S')}@test.com",
            "password": "TestPass123!",
            "name": "Test Admin",
            "role": "admin"
        }
        success, response = self.run_test(
            "Admin Registration",
            "POST",
            "auth/register",
            200,
            data=admin_data
        )
        if success:
            self.tokens['admin'] = response.get('token')
            self.users['admin'] = response.get('user')

    def test_user_login(self):
        """Test user login"""
        print("\n=== Testing User Login ===")
        
        if 'client' in self.users:
            login_data = {
                "email": self.users['client']['email'],
                "password": "TestPass123!"
            }
            success, response = self.run_test(
                "Client Login",
                "POST",
                "auth/login",
                200,
                data=login_data
            )

    def test_auth_me(self):
        """Test getting current user info"""
        print("\n=== Testing Auth Me Endpoint ===")
        
        for role in ['client', 'seller', 'admin']:
            if role in self.tokens:
                success, response = self.run_test(
                    f"Get {role.title()} Info",
                    "GET",
                    "auth/me",
                    200,
                    token=self.tokens[role]
                )

    def test_property_creation(self):
        """Test property creation by seller"""
        print("\n=== Testing Property Creation ===")
        
        if 'seller' not in self.tokens:
            print("❌ No seller token available for property creation test")
            return

        property_data = {
            "title": "Luxury Villa Test Property",
            "description": "A stunning test villa with modern amenities and breathtaking views.",
            "price": 2500000,
            "location": "Beverly Hills, CA",
            "bedrooms": 5,
            "bathrooms": 4,
            "area": 4500.0,
            "property_type": "villa",
            "images": [
                "https://images.pexels.com/photos/3195642/pexels-photo-3195642.jpeg",
                "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg"
            ]
        }
        
        success, response = self.run_test(
            "Create Property (Seller)",
            "POST",
            "properties",
            200,
            data=property_data,
            token=self.tokens['seller']
        )
        
        if success:
            self.properties['test_property'] = response

        # Test client trying to create property (should fail)
        if 'client' in self.tokens:
            success, response = self.run_test(
                "Create Property (Client - Should Fail)",
                "POST",
                "properties",
                403,
                data=property_data,
                token=self.tokens['client']
            )

    def test_property_listing(self):
        """Test property listing with filters"""
        print("\n=== Testing Property Listing ===")
        
        # Test getting all properties
        success, response = self.run_test(
            "Get All Properties",
            "GET",
            "properties",
            200
        )

        # Test with status filter
        success, response = self.run_test(
            "Get Approved Properties",
            "GET",
            "properties?status=approved",
            200
        )

        # Test with multiple filters
        success, response = self.run_test(
            "Get Properties with Filters",
            "GET",
            "properties?property_type=villa&min_price=1000000&bedrooms=5",
            200
        )

    def test_seller_properties(self):
        """Test seller getting their properties"""
        print("\n=== Testing Seller Properties ===")
        
        if 'seller' not in self.tokens:
            print("❌ No seller token available")
            return

        success, response = self.run_test(
            "Get Seller Properties",
            "GET",
            "properties/seller",
            200,
            token=self.tokens['seller']
        )

    def test_property_detail(self):
        """Test getting property details"""
        print("\n=== Testing Property Detail ===")
        
        if 'test_property' not in self.properties:
            print("❌ No test property available")
            return

        property_id = self.properties['test_property']['id']
        success, response = self.run_test(
            "Get Property Detail",
            "GET",
            f"properties/{property_id}",
            200
        )

    def test_lead_creation(self):
        """Test lead creation"""
        print("\n=== Testing Lead Creation ===")
        
        if 'test_property' not in self.properties:
            print("❌ No test property available for lead creation")
            return

        lead_data = {
            "property_id": self.properties['test_property']['id'],
            "name": "John Doe",
            "email": "john.doe@test.com",
            "phone": "+1-555-0123",
            "message": "I'm interested in this property. Please contact me."
        }
        
        success, response = self.run_test(
            "Create Lead",
            "POST",
            "leads",
            200,
            data=lead_data
        )
        
        if success:
            self.leads['test_lead'] = response

    def test_admin_functions(self):
        """Test admin-only functions"""
        print("\n=== Testing Admin Functions ===")
        
        if 'admin' not in self.tokens:
            print("❌ No admin token available")
            return

        # Test analytics
        success, response = self.run_test(
            "Get Analytics",
            "GET",
            "analytics",
            200,
            token=self.tokens['admin']
        )

        # Test getting all leads
        success, response = self.run_test(
            "Get All Leads",
            "GET",
            "leads",
            200,
            token=self.tokens['admin']
        )

        # Test getting all users
        success, response = self.run_test(
            "Get All Users",
            "GET",
            "users",
            200,
            token=self.tokens['admin']
        )

        # Test property approval
        if 'test_property' in self.properties:
            property_id = self.properties['test_property']['id']
            success, response = self.run_test(
                "Approve Property",
                "PATCH",
                f"properties/{property_id}",
                200,
                data={"status": "approved"},
                token=self.tokens['admin']
            )

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        print("\n=== Testing Unauthorized Access ===")
        
        # Test accessing admin endpoints without token
        success, response = self.run_test(
            "Analytics Without Token (Should Fail)",
            "GET",
            "analytics",
            401
        )

        # Test accessing seller endpoints with client token
        if 'client' in self.tokens:
            success, response = self.run_test(
                "Seller Properties with Client Token (Should Fail)",
                "GET",
                "properties/seller",
                403,
                token=self.tokens['client']
            )

def main():
    # Allow base URL to be passed as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else None
    if base_url:
        print(f"🏠 Starting LuxEstate API Testing against {base_url}...")
    else:
        print("🏠 Starting LuxEstate API Testing...")
        print(f"   Using backend URL: {os.environ.get('BACKEND_URL', 'http://localhost:8080')}")
    
    tester = LuxEstateAPITester(base_url=base_url)

    # Run all tests
    tester.test_user_registration()
    tester.test_user_login()
    tester.test_auth_me()
    tester.test_property_creation()
    tester.test_property_listing()
    tester.test_seller_properties()
    tester.test_property_detail()
    tester.test_lead_creation()
    tester.test_admin_functions()
    tester.test_unauthorized_access()

    # Print final results
    print(f"\n📊 Final Results:")
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 Backend API testing completed successfully!")
        return 0
    else:
        print("⚠️ Backend API has significant issues that need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())