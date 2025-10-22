import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';

const { width } = Dimensions.get('window');

const Toast = ({
  visible,
  message,
  type = 'success', // success, error, warning, info
  duration = 3000,
  onHide,
}) => {
  const translateY = new Animated.Value(-100);
  const opacity = new Animated.Value(0);

  useEffect(() => {
    if (visible) {
      // Show animation
      Animated.parallel([
        Animated.timing(translateY, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(opacity, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();

      // Auto hide
      const timer = setTimeout(() => {
        hideToast();
      }, duration);

      return () => clearTimeout(timer);
    } else {
      hideToast();
    }
  }, [visible]);

  const hideToast = () => {
    Animated.parallel([
      Animated.timing(translateY, {
        toValue: -100,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.timing(opacity, {
        toValue: 0,
        duration: 300,
        useNativeDriver: true,
      }),
    ]).start(() => {
      if (onHide) {
        onHide();
      }
    });
  };

  const getToastStyles = () => {
    switch (type) {
      case 'error':
        return {
          backgroundColor: '#dc3545',
          iconName: 'close-circle-outline',
          iconColor: '#fff',
        };
      case 'warning':
        return {
          backgroundColor: '#ffc107',
          iconName: 'warning-outline',
          iconColor: '#000',
        };
      case 'info':
        return {
          backgroundColor: '#007bff',
          iconName: 'information-circle-outline',
          iconColor: '#fff',
        };
      default: // success
        return {
          backgroundColor: '#28a745',
          iconName: 'checkmark-circle-outline',
          iconColor: '#fff',
        };
    }
  };

  const toastStyles = getToastStyles();

  if (!visible) return null;

  return (
    <Animated.View
      style={[
        styles.container,
        {
          backgroundColor: toastStyles.backgroundColor,
          transform: [{ translateY }],
          opacity,
        },
      ]}
    >
      <View style={styles.content}>
        <Icon
          name={toastStyles.iconName}
          size={24}
          color={toastStyles.iconColor}
          style={styles.icon}
        />
        <Text style={[styles.message, { color: toastStyles.iconColor }]}>
          {message}
        </Text>
      </View>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 50,
    left: 20,
    right: 20,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    zIndex: 1000,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  icon: {
    marginRight: 12,
  },
  message: {
    fontSize: 18,
    fontWeight: '600',
    flex: 1,
  },
});

export default Toast;
