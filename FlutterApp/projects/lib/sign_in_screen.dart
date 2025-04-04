import 'package:flutter/material.dart';
import 'sign_up_screen.dart'; // Import the SignUp screen
import 'home_screen.dart'; // Import the HomeScreen

class SignInScreen extends StatelessWidget {
  const SignInScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sign In'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Username Field
            TextField(
              decoration: InputDecoration(labelText: 'Email or Username'),
            ),
            SizedBox(height: 10),

            // Password Field
            TextField(
              obscureText: true,
              decoration: InputDecoration(labelText: 'Password'),
            ),
            SizedBox(height: 20),

            // Sign In Button
            ElevatedButton(
              onPressed: () {
                // Temporary navigation to HomeScreen (You can replace this with real authentication later)
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => HomeScreen()),
                );
              },
              child: Text('Sign In'),
            ),

            // Go to Sign Up Screen
            TextButton(
              onPressed: () {
                // Navigate to the Sign Up screen
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SignUpScreen()),
                );
              },
              child: Text("Don't have an account? Sign Up"),
            ),
          ],
        ),
      ),
    );
  }
}
