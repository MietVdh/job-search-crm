import { Routes, Route, Link } from 'react-router'
import ApplicationsPage from './ApplicationsPage'
import ApplicationDetail from './ApplicationDetail'
import Home from './Home'
 

const NotFound = () => (
  <div>
    <h1>404 - Page Not Found</h1>
    <Link to="/">Go Back Home</Link>
  </div>
)


function App() {

  return (
    <Routes>
      <Route 
        path="/" 
        element={<Home />} 
      />
      <Route 
        path="applications" 
        element={<ApplicationsPage />} 
      />
      <Route 
        path="applications/:applicationId" 
        element={<ApplicationDetail />} 
      />
      <Route 
        path="*"
        element={<NotFound />}
      />
    </Routes>
    
  );
}

export default App
