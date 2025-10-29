import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Modal,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import AIService from '../services/AIService';

const GeminiConfigModal = ({ visible, onClose }) => {
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSaveApiKey = async () => {
    if (!apiKey.trim()) {
      Alert.alert('Erro', 'Por favor, insira sua chave de API do Gemini');
      return;
    }

    setIsLoading(true);

    try {
      // Configurar a chave de API
      AIService.setGeminiApiKey(apiKey.trim());
      
      Alert.alert(
        'Sucesso!',
        'Chave de API do Gemini configurada com sucesso!',
        [
          {
            text: 'OK',
            onPress: () => {
              setApiKey('');
              onClose();
            }
          }
        ]
      );
    } catch (error) {
      Alert.alert('Erro', 'Não foi possível configurar a chave de API');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestApiKey = async () => {
    if (!apiKey.trim()) {
      Alert.alert('Erro', 'Por favor, insira sua chave de API do Gemini');
      return;
    }

    setIsLoading(true);

    try {
      // Testar a chave de API com uma consulta simples
      AIService.setGeminiApiKey(apiKey.trim());
      const testSuggestion = await AIService.getSuggestion('software', 'Teste de conectividade');
      
      Alert.alert(
        'Teste Bem-sucedido!',
        'Sua chave de API do Gemini está funcionando corretamente.',
        [
          {
            text: 'OK',
            onPress: () => {
              setApiKey('');
              onClose();
            }
          }
        ]
      );
    } catch (error) {
      Alert.alert(
        'Erro no Teste',
        'Não foi possível conectar com a API do Gemini. Verifique sua chave de API.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <StatusBar barStyle="light-content" backgroundColor="rgba(0,0,0,0.5)" />
          
          <View style={styles.modalHeader}>
            <View style={styles.headerLeft}>
              <Icon name="bulb-outline" size={24} color="#ffc107" />
              <Text style={styles.modalTitle}>Configurar Gemini Pro</Text>
            </View>
            <TouchableOpacity onPress={onClose}>
              <Icon name="close-circle-outline" size={24} color="#666" />
            </TouchableOpacity>
          </View>

          <View style={styles.modalBody}>
            <Text style={styles.description}>
              Configure sua chave de API do Google Gemini Pro para obter sugestões inteligentes de resolução de problemas.
            </Text>

            <View style={styles.inputContainer}>
              <Icon name="key-outline" size={20} color="#666" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Cole sua chave de API do Gemini aqui"
                placeholderTextColor="#999"
                value={apiKey}
                onChangeText={setApiKey}
                secureTextEntry={true}
                multiline={false}
              />
            </View>

            <View style={styles.infoBox}>
              <Icon name="information-circle-outline" size={20} color="#007bff" />
              <Text style={styles.infoText}>
                Sua chave de API será armazenada localmente no dispositivo e usada apenas para gerar sugestões de resolução.
              </Text>
            </View>

            <View style={styles.instructionsBox}>
              <Text style={styles.instructionsTitle}>Como obter sua chave:</Text>
              <Text style={styles.instructionsText}>
                1. Acesse Google AI Studio (makersuite.google.com){'\n'}
                2. Faça login com sua conta Google{'\n'}
                3. Crie um novo projeto ou selecione um existente{'\n'}
                4. Gere uma nova chave de API{'\n'}
                5. Cole a chave no campo acima
              </Text>
            </View>
          </View>

          <View style={styles.modalFooter}>
            <TouchableOpacity
              style={styles.cancelButton}
              onPress={onClose}
            >
              <Text style={styles.cancelButtonText}>Cancelar</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.testButton}
              onPress={handleTestApiKey}
              disabled={isLoading}
            >
              <Icon name="checkmark-circle-outline" size={20} color="#fff" />
              <Text style={styles.testButtonText}>
                {isLoading ? 'Testando...' : 'Testar'}
              </Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={styles.saveButton}
              onPress={handleSaveApiKey}
              disabled={isLoading}
            >
              <Icon name="save-outline" size={20} color="#fff" />
              <Text style={styles.saveButtonText}>
                {isLoading ? 'Salvando...' : 'Salvar'}
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    width: '100%',
    maxHeight: '80%',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 10,
  },
  modalBody: {
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 20,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#e0e0e0',
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
    fontSize: 16,
    color: '#333',
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: '#e3f2fd',
    padding: 15,
    borderRadius: 8,
    marginBottom: 20,
  },
  infoText: {
    flex: 1,
    fontSize: 12,
    color: '#1976d2',
    marginLeft: 10,
    lineHeight: 16,
  },
  instructionsBox: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007bff',
  },
  instructionsTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  instructionsText: {
    fontSize: 12,
    color: '#666',
    lineHeight: 18,
  },
  modalFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  cancelButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#6c757d',
    alignItems: 'center',
    marginRight: 10,
  },
  cancelButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  testButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#28a745',
    marginRight: 10,
  },
  testButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    marginLeft: 5,
  },
  saveButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#007bff',
  },
  saveButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    marginLeft: 5,
  },
});

export default GeminiConfigModal;

