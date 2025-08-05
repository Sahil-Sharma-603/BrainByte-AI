import ClerkProviderWithRoutes from './auth/ClerkProviderWithRoutes';
import {Routes, Route} from 'react-router-dom'
import {AuthenticationPage} from './auth/AuthenticationPage'
import {Layout} from './layout/Layout'
import {HistoryPanel} from './history/HistoryPanel'
import {ChallengeGenerator} from './challenge/ChallengeGenerator'

import './App.css'

function App() {
  
  return <ClerkProviderWithRoutes>

      <Routes>
        <Route path = "/sign-in/*" element={<AuthenticationPage/>} />
        <Route path = "/sign-up/*" element={<AuthenticationPage/>} />
    
        <Route element = {<Layout/>}>
          <Route path = "/history" element={<HistoryPanel/>} />
          <Route path = "/" element={<ChallengeGenerator/>} />
        </Route>

      </Routes>

  </ClerkProviderWithRoutes>     
}

export default App
