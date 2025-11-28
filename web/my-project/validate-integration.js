#!/usr/bin/env node

/**
 * API Integration Validation Script
 * Run: node validate-integration.js
 * 
 * This script validates all API endpoints used by the Reports and Users pages
 */

const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZW1haWwiOiJhZG1pbjJAaGVscHdhdmUuY29tIiwicm9sZSI6IkFkbWluaXN0cmFkb3IiLCJleHAiOjE3NjM4NzIyMTAsImlzcyI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCIsImF1ZCI6Imh0dHBzOi8vYXBpLXN1cG9ydGUtZ3J1cG8tYmhnaGd1YTVoYmQ0ZTVoay5icmF6aWxzb3V0aC0wMS5henVyZXdlYnNpdGVzLm5ldCJ9.YgNgT7Fz0_OSUGdULhWZrAjpnp5csUfFFxuknQAZog4';
const API_URL = 'http://localhost:5000';

const endpoints = [
  {
    name: 'Get All Users',
    method: 'GET',
    url: `${API_URL}/api/Usuarios`,
    description: 'Used by: UsersReportPage - fetches all users list'
  },
  {
    name: 'Get User by ID (3) [Endpoint may return 404 - will use fallback]',
    method: 'GET',
    url: `${API_URL}/api/Usuarios/3`,
    description: 'Used by: UserActivityPage - fetches user profile (fallback: searches in user list)'
  },
  {
    name: 'Get Current User Profile',
    method: 'GET',
    url: `${API_URL}/api/Usuarios/meu-perfil`,
    description: 'Used by: Auth service - gets logged-in user details'
  },
  {
    name: 'Get All Tickets',
    method: 'GET',
    url: `${API_URL}/chamados`,
    description: 'Used by: UserActivityPage - fetches all tickets'
  },
  {
    name: 'Get Tickets by User (solicitanteId=5)',
    method: 'GET',
    url: `${API_URL}/chamados?solicitanteId=5`,
    description: 'Used by: UserActivityPage - fetches tickets opened by user'
  },
  {
    name: 'Get Single Ticket (1)',
    method: 'GET',
    url: `${API_URL}/chamados/1`,
    description: 'Used by: Call Details page - fetches single ticket'
  }
];

async function testEndpoint(endpoint) {
  console.log(`\n📍 Testing: ${endpoint.name}`);
  console.log(`   Description: ${endpoint.description}`);
  console.log(`   Method: ${endpoint.method} ${endpoint.url}`);
  
  try {
    const response = await fetch(endpoint.url, {
      method: endpoint.method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    
    if (response.ok) {
      console.log(`   ✅ Status: ${response.status} OK`);
      
      // Show response structure
      if (Array.isArray(data)) {
        console.log(`   📊 Response: Array with ${data.length} items`);
        if (data.length > 0) {
          console.log(`      First item keys: ${Object.keys(data[0]).join(', ')}`);
        }
      } else if (typeof data === 'object' && data !== null) {
        const keys = Object.keys(data);
        console.log(`   📊 Response: Object with ${keys.length} properties`);
        console.log(`      Keys: ${keys.slice(0, 5).join(', ')}${keys.length > 5 ? ', ...' : ''}`);
      }
      
      return { status: 'success', code: response.status, data };
    } else {
      console.log(`   ❌ Status: ${response.status} ${response.statusText}`);
      console.log(`      Error: ${data.message || JSON.stringify(data).substring(0, 100)}`);
      return { status: 'error', code: response.status, data };
    }
  } catch (error) {
    console.log(`   ❌ Connection Error: ${error.message}`);
    return { status: 'error', code: 0, error: error.message };
  }
}

async function validateIntegration() {
  console.log('\n🔍 HelpWave API Integration Validation\n');
  console.log('=' .repeat(60));
  console.log('Testing all endpoints required by Reports & Users pages');
  console.log('=' .repeat(60));
  
  const results = [];
  
  for (const endpoint of endpoints) {
    const result = await testEndpoint(endpoint);
    results.push({ endpoint: endpoint.name, result });
    // Add small delay between requests
    await new Promise(r => setTimeout(r, 300));
  }
  
  // Summary
  console.log('\n' + '=' .repeat(60));
  console.log('📋 SUMMARY\n');
  
  const successful = results.filter(r => r.result.status === 'success');
  const failed = results.filter(r => r.result.status === 'error');
  
  console.log(`Total Endpoints: ${results.length}`);
  console.log(`✅ Successful: ${successful.length}`);
  console.log(`❌ Failed: ${failed.length}`);
  
  if (failed.length > 0) {
    console.log('\n⚠️ Failed Endpoints:');
    failed.forEach(r => {
      console.log(`  - ${r.endpoint}`);
      console.log(`    Code: ${r.result.code}`);
    });
  } else {
    console.log('\n🎉 All endpoints are working correctly!');
  }
  
  console.log('\n' + '=' .repeat(60) + '\n');
}

// Run validation
validateIntegration().catch(console.error);
