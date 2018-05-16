import axios from 'axios'

const baseURL = process.env.REACT_APP_BACKEND_HOST || 'http://localhost:8000'

export const ITEMS = '/items/'

export const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// TODO: hide all API logic from App.js here
