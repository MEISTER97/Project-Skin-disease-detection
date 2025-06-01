import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import 'sign_up_screen.dart'; // Import the SignUp screen
import 'home_screen.dart'; // Import the HomeScreen
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import 'package:SkinAI/utils/config.dart';

// Create storage instance
final secureStorage = FlutterSecureStorage();


class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _isLoading = false;

  // This function handles login
  Future<void> _signIn() async {
    final email = _usernameController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter both email and password.')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final url = Uri.parse('$BASE_URL/api/token/');
      final response = await http
          .post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      )
          .timeout(
        const Duration(seconds: 10),
        onTimeout: () => throw TimeoutException('Login Request timed out'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final accessToken = data['access'];
        final refreshToken = data['refresh'];

        // 🔐 Store tokens securely
        await secureStorage.write(key: 'access_token', value: accessToken);
        await secureStorage.write(key: 'refresh_token', value: refreshToken);

        print('Access Token Saved: $accessToken');

        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => HomeScreen()),
        );
      } else {
        print('Login failed: ${response.body}');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Login failed. Please check credentials.')),
        );
      }
    } on TimeoutException catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login request timed out. Please try again.')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('An error occurred: $e')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          'Sign In',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 24,
            color: Colors.white, // High contrast on dark overlay
            letterSpacing: 1.0,  // Optional: adds emphasis
          ),
        ),
        iconTheme: IconThemeData(color: Colors.white), // Ensures back button is visible
      ),
      extendBodyBehindAppBar: true, // allows content to go behind the app bar
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Background Image
          Image.asset(
            'assets/login_background.jpg',
            fit: BoxFit.cover,
          ),

          // Optional dark overlay for readability
          Container(color: Colors.black.withOpacity(0.2)),

          // Form content
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Center(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    TextField(
                      controller: _usernameController,
                      decoration: InputDecoration(
                        labelText: 'Email or Username',
                        filled: true,
                        fillColor: Colors.white70,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                    SizedBox(height: 10),
                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        filled: true,
                        fillColor: Colors.white70,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    _isLoading
                        ? CircularProgressIndicator()
                        : ElevatedButton(
                      onPressed: _signIn,
                      child: Text('Sign In'),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (context) => SignUpScreen()),
                        );
                      },
                      child: Text("Don't have an account? Sign Up"),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.black,
                      ),
                    ),

                    TextButton(
                      onPressed: () async {
                        final guestId = const Uuid().v4(); // generate random guest ID
                        await secureStorage.write(key: 'guest_session_id', value: guestId);

                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (context) => HomeScreen(isGuest: true)),
                        );
                      },
                      child: Text("Continue as Guest"),
                    ),

                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

}
