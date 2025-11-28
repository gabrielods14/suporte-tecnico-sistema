import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import ConfirmationModal from '../components/ConfirmationModal';
import LoadingOverlay from '../components/LoadingOverlay';
import ApiService from '../services/api';

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showForgotPasswordModal, setShowForgotPasswordModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos');
      return;
    }

    setIsLoading(true);

    try {
      console.log('Iniciando processo de login...');
      console.log('Email:', email);
      console.log('Password:', password ? '***' : 'vazia');
      
      // Fazer login usando a API real
      const response = await ApiService.login(email, password);
      
      console.log('Resposta do login:', response);
      
      // A API retorna "Token" com T maiúsculo (conforme LoginResponseDto)
      const token = response?.Token || response?.token;
      if (response && token) {
        console.log('Login bem-sucedido! Navegando para Home...');
        // Login bem-sucedido, navegar para a tela home
        navigation.navigate('Home');
      } else {
        console.log('Erro: Nenhum token recebido');
        Alert.alert('Erro', 'Erro no login. Tente novamente.');
      }
    } catch (error) {
      console.log('Erro capturado no handleLogin:', error);
      console.log('Mensagem do erro:', error.message);
      
      let errorMessage = 'Erro ao fazer login. Verifique suas credenciais.';
      
      if (error.message.includes('Network request failed')) {
        errorMessage = 'Erro de conexão. Verifique sua internet e tente novamente.';
      } else if (error.message.includes('E-mail ou senha inválidos')) {
        errorMessage = 'E-mail ou senha inválidos. Verifique suas credenciais.';
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      Alert.alert('Erro', errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = () => {
    setShowForgotPasswordModal(true);
  };

  const confirmForgotPassword = () => {
    setShowForgotPasswordModal(false);
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <StatusBar barStyle="light-content" backgroundColor="#1a1a1a" />
      
      {/* Hero Section */}
      <View style={styles.hero}>
        <Text style={styles.heroText}>HelpWave - Simplificando o seu suporte.</Text>
      </View>

      {/* Login Form */}
      <View style={styles.formContainer}>
        <View style={styles.form}>
          <Text style={styles.title}>LOGIN</Text>
          
          <View style={styles.inputContainer}>
            <Icon name="person-outline" size={20} color="#bbb" style={styles.inputIcon} />
            <TextInput
              style={styles.input}
              placeholder="USUÁRIO"
              placeholderTextColor="#bbb"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
          </View>
          
          <View style={styles.inputContainer}>
            <Icon name="lock-closed-outline" size={20} color="#bbb" style={styles.inputIcon} />
            <TextInput
              style={styles.input}
              placeholder="SENHA"
              placeholderTextColor="#bbb"
              value={password}
              onChangeText={setPassword}
              secureTextEntry={!showPassword}
            />
            <TouchableOpacity 
              style={styles.eyeIcon} 
              onPress={() => setShowPassword(!showPassword)}
            >
              <Icon 
                name={showPassword ? "eye-outline" : "eye-off-outline"} 
                size={20} 
                color="#bbb" 
              />
            </TouchableOpacity>
          </View>
          
          <TouchableOpacity 
            style={[styles.button, isLoading && styles.buttonDisabled]} 
            onPress={handleLogin}
            disabled={isLoading}
          >
            <Text style={styles.buttonText}>
              {isLoading ? 'ENTRANDO...' : 'ENTRAR'}
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={styles.forgotPasswordButton}
            onPress={handleForgotPassword}
          >
            <Text style={styles.forgotPasswordText}>Esqueci minha senha</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Forgot Password Confirmation Modal */}
      <ConfirmationModal
        visible={showForgotPasswordModal}
        onClose={() => setShowForgotPasswordModal(false)}
        onConfirm={confirmForgotPassword}
        title="Recuperar Senha"
        message="Para alterar sua senha, entre em contato com seu superior ou administrador do sistema. Eles poderão ajudá-lo a redefinir sua senha de acesso de forma segura."
        confirmText="Entendi"
        cancelText="Cancelar"
        confirmColor="#28a745"
        iconName="shield-checkmark-outline"
        iconColor="#28a745"
        type="info"
      />

      {/* Loading Overlay */}
      <LoadingOverlay
        visible={isLoading}
        message="Fazendo login..."
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
  },
  hero: {
    backgroundColor: '#8B0000',
    paddingVertical: 60,
    paddingHorizontal: 30,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 200,
  },
  heroText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    lineHeight: 36,
  },
  formContainer: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    paddingHorizontal: 20,
    paddingVertical: 40,
    justifyContent: 'center',
  },
  form: {
    backgroundColor: 'transparent',
    paddingHorizontal: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 40,
    color: '#fff',
    letterSpacing: 2,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#333',
    borderRadius: 8,
    marginBottom: 20,
    borderWidth: 2,
    borderColor: '#555',
  },
  inputIcon: {
    position: 'absolute',
    left: 15,
    zIndex: 1,
  },
  input: {
    flex: 1,
    paddingHorizontal: 50,
    paddingVertical: 15,
    fontSize: 18,
    color: '#fff',
  },
  eyeIcon: {
    position: 'absolute',
    right: 15,
    padding: 5,
  },
  button: {
    backgroundColor: '#dc3545',
    paddingVertical: 16,
    paddingHorizontal: 20,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
    shadowColor: '#dc3545',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 5,
  },
  buttonDisabled: {
    backgroundColor: '#6c757d',
    shadowOpacity: 0,
  },
  buttonText: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  forgotPasswordButton: {
    marginTop: 20,
    alignItems: 'center',
    paddingVertical: 10,
  },
  forgotPasswordText: {
    color: '#ffc107',
    fontSize: 18,
    textDecorationLine: 'underline',
    fontWeight: '500',
  },
});

export default LoginScreen;
