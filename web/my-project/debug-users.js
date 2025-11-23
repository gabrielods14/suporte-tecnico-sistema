#!/usr/bin/env node

/**
 * Quick Debug Script - Test Users Report Data Loading
 * Usage: node debug-users.js
 */

const API_URL = 'http://localhost:5000';

// Seu token JWT (copie do browser ou do teste anterior)
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZW1haWwiOiJhZG1pbjJAaGVscHdhdmUuY29tIiwicm9sZSI6IkFkbWluaXN0cmFkb3IiLCJleHAiOjE3NjM4NzIyMTAsImlzcyI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCIsImF1ZCI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCJ9.YgNgT7Fz0_OSUGdULhWZrAjpnp5csUfFFxuknQAZog4';

async function testDataLoading() {
  console.log('\n🔍 HelpWave Users Report - Data Loading Debug\n');
  console.log('='.repeat(60));
  
  try {
    console.log('📡 Fetching from: GET /api/Usuarios\n');
    
    const response = await fetch(`${API_URL}/api/Usuarios`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      console.log(`❌ Error: ${response.status} ${response.statusText}`);
      return;
    }

    const data = await response.json();
    console.log('✅ Response received\n');
    
    // Show response structure
    console.log('📊 Response Structure:');
    console.log(`   - Type: ${typeof data}`);
    console.log(`   - Keys: ${Object.keys(data).join(', ')}`);
    
    // Extract usuarios
    let usuarios = [];
    if (data.usuarios && Array.isArray(data.usuarios)) {
      usuarios = data.usuarios;
      console.log(`\n📋 Found: usuarios array with ${usuarios.length} items\n`);
    } else if (Array.isArray(data)) {
      usuarios = data;
      console.log(`\n📋 Found: direct array with ${usuarios.length} items\n`);
    }

    if (usuarios.length === 0) {
      console.log('⚠️ No users found in response!');
      console.log('Full response:', JSON.stringify(data, null, 2));
      return;
    }

    // Show users table
    console.log('📑 Users List:\n');
    console.log('┌─────────────────────────────────────────────────────────────┐');
    console.log('│  ID  │        NOME        │         E-MAIL         │ CARGO  │');
    console.log('├─────────────────────────────────────────────────────────────┤');
    
    usuarios.forEach(u => {
      const id = String(u.id).padEnd(4);
      const nome = (u.nome || 'N/A').substring(0, 18).padEnd(18);
      const email = (u.email || 'N/A').substring(0, 22).padEnd(22);
      const cargo = (u.cargo || 'N/A').substring(0, 10);
      console.log(`│ ${id} │ ${nome} │ ${email} │ ${cargo} │`);
    });
    
    console.log('└─────────────────────────────────────────────────────────────┘\n');

    // Show first user details
    const firstUser = usuarios[0];
    console.log('🔍 First User (Full Details):\n');
    console.log(`   ID:        ${firstUser.id}`);
    console.log(`   Nome:      ${firstUser.nome}`);
    console.log(`   Email:     ${firstUser.email}`);
    console.log(`   Cargo:     ${firstUser.cargo}`);
    console.log(`   Permissão: ${firstUser.permissao} (${getPermissaoLabel(firstUser.permissao)})`);
    console.log(`   Telefone:  ${firstUser.telefone}\n`);

    console.log('='.repeat(60));
    console.log('\n✅ Data loading test completed successfully!\n');
    console.log('📌 What to expect in Frontend:');
    console.log(`   - Users table should show ${usuarios.length} rows`);
    console.log('   - Click on any row to view user activity');
    console.log('   - Search should filter by ID, name, or email\n');

  } catch (error) {
    console.log(`\n❌ Error: ${error.message}\n`);
    console.log('Troubleshooting:');
    console.log('1. Ensure API is running on port 5000');
    console.log('2. Check token is valid and not expired');
    console.log('3. User must have Admin or Suporte Técnico role\n');
  }
}

function getPermissaoLabel(perm) {
  const p = Number(perm);
  if (p === 1) return 'Colaborador';
  if (p === 2) return 'Suporte Técnico';
  if (p === 3) return 'Administrador';
  return 'Desconhecido';
}

testDataLoading();
