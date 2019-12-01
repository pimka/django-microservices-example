import axios from 'axios'

const token = localStorage.getItem('token')
export const HTTP = axios.create({
  baseURL: 'http://localhost:8081/',
  headers: {
    'Authorization': token
  }
})
