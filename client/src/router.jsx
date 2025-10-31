import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import ProtectedRoute from "./components/ProtectedRoute";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import OnboardingPage from "./pages/OnboardingPage";

import ChequeUploadPage from "./pages/ChequeUploadPage";
import ChequeDetailPage from "./pages/ChequeDetailPage";
import ChequeListPage from "./pages/ChequeListPage";
import VerificationListPage from "./pages/VerificationListPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <ChequeListPage /> },
      { path: "login", element: <LoginPage /> },
      { path: "register", element: <RegisterPage /> },
      { path: "onboarding", element: <OnboardingPage /> },

      // protected block
      {
        element: <ProtectedRoute />,
        children: [
          { path: "upload", element: <ChequeUploadPage /> },
          { path: "cheques", element: <ChequeListPage /> },
          { path: "cheques/:id", element: <ChequeDetailPage /> },
          { path: "verifications", element: <VerificationListPage /> },
        ],
      },
    ],
  },
]);

export default router;
