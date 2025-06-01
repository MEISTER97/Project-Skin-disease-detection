import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:SkinAI/sign_in_screen.dart';
import 'dart:async';

// Make sure you have this screen created

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with TickerProviderStateMixin {
  late AnimationController _sizeController; // Controller for size animation
  late AnimationController _positionController; // Controller for position animation

  double _height = 200; // Initial height of the animation
  double _width = 200; // Initial width of the animation
  double _topPosition = 0; // Initial position (at the top)

  @override
  void initState() {
    super.initState();

    // Controller for size animation (from smaller size to larger)
    _sizeController = AnimationController(
      duration: Duration(seconds: 2), // Speed up size growth
      vsync: this,
    )..addListener(() {
      setState(() {
        _height = 200 + _sizeController.value * 100; // Grow height
        _width = 200 + _sizeController.value * 100;  // Grow width
      });
    });

    // Controller for position animation (from bottom to center, faster movement)
    _positionController = AnimationController(
      duration: Duration(seconds: 2), // Faster position animation
      vsync: this,
    )..addListener(() {
      setState(() {
        _topPosition = _positionController.value * 300; // Move up to center quickly
      });
    });

    // Start both animations simultaneously
    _sizeController.forward();
    _positionController.forward();

    // Wait for 3 seconds and navigate to Home Screen
    Timer(Duration(seconds: 3), () {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => SignInScreen()), // Go to SignInScreen
      );
    });
  }

  @override
  void dispose() {
    _sizeController.dispose();
    _positionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent, // Let background image show
      body: Stack(
        children: [
          // Background Image
          Positioned.fill(
            child: Image.asset(
              'assets/start_screen_background.jpg',
              fit: BoxFit.cover,
            ),
          ),

          // Optional overlay for contrast
          Positioned.fill(
            child: Container(color: Colors.black.withOpacity(0.2)),
          ),

          // Lottie Animation (centered and animated)
          Positioned(
            top: _topPosition,
            left: MediaQuery.of(context).size.width / 2 - _width / 2,
            child: AnimatedSize(
              duration: Duration(seconds: 2),
              curve: Curves.easeInOut,
              child: Lottie.asset(
                'assets/Animation_medical.json',
                width: _width,
                height: _height,
                fit: BoxFit.contain,
              ),
            ),
          ),
        ],
      ),
    );
  }

}
