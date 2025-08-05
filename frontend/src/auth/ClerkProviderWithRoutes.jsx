
import { ClerkProvider } from '@clerk/clerk-react'
import {BrowserRotuer} from 'react-router-dom'

// Import your Publishable Key from environment Variables
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Publishable Key')
}

// Create a ClerkProviderWithRoutes component that wraps children with ClerkProvider and BrowserRouter
export default function ClerkProviderWithRoutes({ children }) {
  return (
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <BrowserRotuer> {children} </BrowserRotuer>
    </ClerkProvider>
  )
}


