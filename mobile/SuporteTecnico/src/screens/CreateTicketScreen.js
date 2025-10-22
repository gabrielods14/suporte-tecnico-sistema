import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  StatusBar,
  Alert,
  Modal,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useTickets } from '../context/TicketContext';
import ConfirmationModal from '../components/ConfirmationModal';
import Toast from '../components/Toast';
import LoadingOverlay from '../components/LoadingOverlay';

const CreateTicketScreen = ({ navigation }) => {
  const [selectedProblemType, setSelectedProblemType] = useState('');
  const [description, setDescription] = useState('');
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');
  const { createTicket } = useTickets();

  const problemTypes = [
    { id: 'hardware', label: 'Problema de Hardware', icon: 'hardware-chip-outline' },
    { id: 'software', label: 'Problema de Software', icon: 'desktop-outline' },
    { id: 'network', label: 'Problema de Rede', icon: 'wifi-outline' },
    { id: 'printer', label: 'Problema com Impressora', icon: 'print-outline' },
    { id: 'email', label: 'Problema com Email', icon: 'mail-outline' },
    { id: 'password', label: 'Reset de Senha', icon: 'key-outline' },
    { id: 'access', label: 'Solicitação de Acesso', icon: 'lock-closed-outline' },
    { id: 'other', label: 'Outros', icon: 'help-circle-outline' },
  ];

  const showToastMessage = (message, type = 'success') => {
    setToastMessage(message);
    setToastType(type);
    setShowToast(true);
  };

  const handleSubmit = async () => {
    if (!selectedProblemType || !description.trim()) {
      showToastMessage('Por favor, preencha todos os campos obrigatórios', 'error');
      return;
    }

    if (description.trim().length < 10) {
      showToastMessage('A descrição deve ter pelo menos 10 caracteres', 'error');
      return;
    }

    setIsLoading(true);

    try {
      // Criar o chamado usando o contexto
      const problemTypeLabel = problemTypes.find(type => type.id === selectedProblemType)?.label || 'Outros';
      
      createTicket({
        title: problemTypeLabel,
        type: selectedProblemType,
        description: description.trim(),
        user: 'Usuário Atual',
        userEmail: 'usuario@empresa.com',
        priority: 'Média',
      });
      
      showToastMessage('Chamado criado com sucesso!', 'success');
      
      // Aguardar um pouco para mostrar o toast, depois limpar e voltar
      setTimeout(() => {
        setSelectedProblemType('');
        setDescription('');
        navigation.goBack();
      }, 1500);
      
    } catch (error) {
      showToastMessage('Não foi possível criar o chamado. Tente novamente.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const getSelectedProblemTypeLabel = () => {
    const selected = problemTypes.find(type => type.id === selectedProblemType);
    return selected ? selected.label : 'Selecione o tipo de problema';
  };

  const getSelectedProblemTypeIcon = () => {
    const selected = problemTypes.find(type => type.id === selectedProblemType);
    return selected ? selected.icon : 'chevron-down-outline';
  };

  const hasUnsavedChanges = () => {
    return selectedProblemType !== '' || description.trim() !== '';
  };

  const handleBackPress = () => {
    if (hasUnsavedChanges()) {
      setShowCancelModal(true);
    } else {
      navigation.goBack();
    }
  };

  const confirmCancel = () => {
    setShowCancelModal(false);
    navigation.goBack();
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#dc3545" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={handleBackPress}
        >
          <Icon name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Abrir Chamado</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Form Section */}
        <View style={styles.formSection}>
          <View style={styles.sectionHeader}>
            <Icon name="create-outline" size={20} color="#dc3545" />
            <Text style={styles.sectionTitle}>Informações do Chamado</Text>
          </View>

          {/* Problem Type Selection */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Tipo de Problema *</Text>
            <TouchableOpacity 
              style={styles.dropdownButton}
              onPress={() => setIsDropdownOpen(true)}
            >
              <View style={styles.dropdownContent}>
                <Icon name={getSelectedProblemTypeIcon()} size={20} color="#666" />
                <Text style={[
                  styles.dropdownText,
                  selectedProblemType ? styles.dropdownTextSelected : styles.dropdownTextPlaceholder
                ]}>
                  {getSelectedProblemTypeLabel()}
                </Text>
              </View>
              <Icon name="chevron-down-outline" size={20} color="#666" />
            </TouchableOpacity>
          </View>

          {/* Description Field */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Descrição do Problema *</Text>
            <TextInput
              style={styles.textArea}
              placeholder="Descreva detalhadamente o problema que você está enfrentando..."
              placeholderTextColor="#999"
              value={description}
              onChangeText={setDescription}
              multiline
              numberOfLines={6}
              textAlignVertical="top"
            />
            <Text style={styles.characterCount}>
              {description.length}/500 caracteres
            </Text>
          </View>

          {/* Submit Button */}
          <TouchableOpacity 
            style={[styles.submitButton, isLoading && styles.submitButtonDisabled]} 
            onPress={handleSubmit}
            disabled={isLoading}
          >
            <Icon name="send-outline" size={20} color="#fff" />
            <Text style={styles.submitButtonText}>
              {isLoading ? 'Criando Chamado...' : 'Criar Chamado'}
            </Text>
          </TouchableOpacity>
        </View>

        {/* Help Section */}
        <View style={styles.helpSection}>
          <View style={styles.sectionHeader}>
            <Icon name="information-circle-outline" size={20} color="#dc3545" />
            <Text style={styles.sectionTitle}>Dicas para um Chamado Eficiente</Text>
          </View>
          
          <View style={styles.tipItem}>
            <Icon name="checkmark-circle-outline" size={16} color="#28a745" />
            <Text style={styles.tipText}>Seja específico sobre o problema</Text>
          </View>
          
          <View style={styles.tipItem}>
            <Icon name="checkmark-circle-outline" size={16} color="#28a745" />
            <Text style={styles.tipText}>Inclua mensagens de erro se houver</Text>
          </View>
          
          <View style={styles.tipItem}>
            <Icon name="checkmark-circle-outline" size={16} color="#28a745" />
            <Text style={styles.tipText}>Mencione quando o problema começou</Text>
          </View>
          
          <View style={styles.tipItem}>
            <Icon name="checkmark-circle-outline" size={16} color="#28a745" />
            <Text style={styles.tipText}>Descreva o que você já tentou fazer</Text>
          </View>
        </View>
      </ScrollView>

      {/* Problem Type Modal */}
      <Modal
        visible={isDropdownOpen}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setIsDropdownOpen(false)}
      >
        <TouchableOpacity 
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setIsDropdownOpen(false)}
        >
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Selecione o Tipo de Problema</Text>
              <TouchableOpacity onPress={() => setIsDropdownOpen(false)}>
                <Icon name="close-outline" size={24} color="#666" />
              </TouchableOpacity>
            </View>
            
            <ScrollView style={styles.optionsList}>
              {problemTypes.map((type) => (
                <TouchableOpacity
                  key={type.id}
                  style={[
                    styles.optionItem,
                    selectedProblemType === type.id && styles.optionItemSelected
                  ]}
                  onPress={() => {
                    setSelectedProblemType(type.id);
                    setIsDropdownOpen(false);
                  }}
                >
                  <Icon 
                    name={type.icon} 
                    size={20} 
                    color={selectedProblemType === type.id ? "#dc3545" : "#666"} 
                  />
                  <Text style={[
                    styles.optionText,
                    selectedProblemType === type.id && styles.optionTextSelected
                  ]}>
                    {type.label}
                  </Text>
                  {selectedProblemType === type.id && (
                    <Icon name="checkmark-outline" size={20} color="#dc3545" />
                  )}
                </TouchableOpacity>
              ))}
            </ScrollView>
          </View>
        </TouchableOpacity>
      </Modal>

      {/* Cancel Confirmation Modal */}
      <ConfirmationModal
        visible={showCancelModal}
        onClose={() => setShowCancelModal(false)}
        onConfirm={confirmCancel}
        title="Cancelar Criação"
        message="Você tem alterações não salvas. Tem certeza que deseja sair? Todas as informações preenchidas serão perdidas."
        confirmText="Sair"
        cancelText="Continuar Editando"
        confirmColor="#dc3545"
        iconName="warning-outline"
        iconColor="#ffc107"
        type="warning"
      />

      {/* Toast Notification */}
      <Toast
        visible={showToast}
        message={toastMessage}
        type={toastType}
        onHide={() => setShowToast(false)}
      />

      {/* Loading Overlay */}
      <LoadingOverlay
        visible={isLoading}
        message="Criando chamado..."
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#dc3545',
    paddingHorizontal: 20,
    paddingVertical: 15,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  backButton: {
    padding: 8,
    borderRadius: 6,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 16,
  },
  headerSpacer: {
    width: 40,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  formSection: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 10,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  dropdownButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#f8f9fa',
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
  },
  dropdownContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  dropdownText: {
    fontSize: 18,
    marginLeft: 10,
    flex: 1,
  },
  dropdownTextSelected: {
    color: '#333',
  },
  dropdownTextPlaceholder: {
    color: '#999',
  },
  textArea: {
    backgroundColor: '#f8f9fa',
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 18,
    color: '#333',
    minHeight: 120,
  },
  characterCount: {
    fontSize: 14,
    color: '#666',
    textAlign: 'right',
    marginTop: 5,
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc3545',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginTop: 10,
    shadowColor: '#dc3545',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  submitButtonDisabled: {
    backgroundColor: '#6c757d',
    shadowOpacity: 0,
  },
  submitButtonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
    marginLeft: 8,
  },
  helpSection: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  tipItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  tipText: {
    fontSize: 16,
    color: '#666',
    marginLeft: 10,
    flex: 1,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    width: '90%',
    maxHeight: '70%',
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
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
  },
  optionsList: {
    maxHeight: 300,
  },
  optionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f8f9fa',
  },
  optionItemSelected: {
    backgroundColor: '#fff5f5',
  },
  optionText: {
    fontSize: 18,
    color: '#333',
    marginLeft: 15,
    flex: 1,
  },
  optionTextSelected: {
    color: '#dc3545',
    fontWeight: '600',
  },
});

export default CreateTicketScreen;
