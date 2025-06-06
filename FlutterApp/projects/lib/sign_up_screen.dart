import 'dart:async';
import 'dart:convert';
import 'package:SkinAI/sign_in_screen.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'home_screen.dart';
import 'package:SkinAI/utils/config.dart';


class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _isLoading = false;

  /// Signs up a new user by sending their email & password to the backend.
  /// On successful registration, automatically logs the user in and navigates to HomeScreen.
  /// Displays helpful messages to guide the user through the process.
  Future<void> _signUp() async {
    // Read user input
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    // Basic validation
    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter both email and password')),
      );
      return;
    }

    setState(() => _isLoading = true); // Show loading indicator

    try {
      // Step 1: Register the user
      final url = Uri.parse('$BASE_URL/api/register/');
      final response = await http
          .post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      )
          .timeout(
        const Duration(seconds: 10),
        onTimeout: () => throw TimeoutException('Registration request timed out'),
      );

      if (response.statusCode == 201) {
        // ✅ Registration successful → Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Registration successful! Logging in...')),
        );

        // Small delay so user sees message before auto login starts
        await Future.delayed(Duration(milliseconds: 1200));

        // Step 2: Log the user in automatically
        final loginUrl = Uri.parse('$BASE_URL/api/token/');
        final loginResponse = await http
            .post(
          loginUrl,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'email': email, 'password': password}),
        )
            .timeout(
          const Duration(seconds: 10),
          onTimeout: () => throw TimeoutException('Login request timed out'),
        );

        if (loginResponse.statusCode == 200) {
          // Parse tokens
          final data = jsonDecode(loginResponse.body);
          final accessToken = data['access'];
          final refreshToken = data['refresh'];

          // 🔐 Save tokens securely
          await secureStorage.write(key: 'access_token', value: accessToken);
          await secureStorage.write(key: 'refresh_token', value: refreshToken);

          // ✅ Optional: Show login success message
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Login successful! Welcome.')),
          );

          // Small delay so user sees message before navigating
          await Future.delayed(Duration(milliseconds: 1000));

          // Navigate to HomeScreen
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => HomeScreen()),
          );
        } else {
          // If login after registration failed
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Login after sign-up failed.')),
          );
        }
      } else {
        // If registration failed → show error message from server
        final error = jsonDecode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Registration failed: ${error.toString()}')),
        );
      }
    } on TimeoutException catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.message ?? 'Request timed out')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('An error occurred: $e')),
      );
    } finally {
      // Hide loading indicator
      setState(() => _isLoading = false);
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          'Sign Up',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 24,
            color: Colors.white,
            letterSpacing: 1.0,
          ),
        ),
        iconTheme: IconThemeData(color: Colors.white),
      ),

      extendBodyBehindAppBar: true,
      body: Stack(
        fit: StackFit.expand,
        children: [
          // Background image
          Image.asset(
            'assets/signup_background.jpg',
            fit: BoxFit.cover,
          ),


          // Form content
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Center(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    TextField(
                      controller: _emailController,
                      decoration: InputDecoration(
                        labelText: 'Email',
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
                    ElevatedButton(
                      onPressed: _isLoading ? null : _signUp,
                      child: Text(_isLoading ? 'Signing Up...' : 'Sign Up'),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                      ),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (context) => SignInScreen()),
                        );
                      },
                      child: Text("Already have an account? Sign In"),
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.white70,
                      ),
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
