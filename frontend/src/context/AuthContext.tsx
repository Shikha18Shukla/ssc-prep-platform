/**
 * React Context providing authentication state across the application.
 */

import React, { createContext, useContext, useEffect, useState } from "react";
import { User } from "@/types";
import { ApiError } from "@/services/api";
import {
  getCachedUser,
  getCurrentUser,
  getToken,
  login as apiLogin,
  logout as apiLogout,
  register as apiRegister,
  LoginPayload,
  RegisterPayload,
} from "@/services/auth";

export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<User>;
  register: (payload: RegisterPayload) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(getToken());
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const handleExpiredSession = () => {
      apiLogout();
      setUser(null);
      setToken(null);
    };
    window.addEventListener("ssc-auth-expired", handleExpiredSession);

    async function initAuth() {
      const activeToken = getToken();
      if (!activeToken) {
        setIsLoading(false);
        return;
      }

      const cachedUser = getCachedUser();
      if (cachedUser) setUser(cachedUser);

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
        setToken(activeToken);
      } catch (error) {
        // Preserve an otherwise valid session through Render/Neon cold starts or
        // short network outages. Clear it only when the server rejects the token.
        if (error instanceof ApiError && (error.status === 401 || error.status === 403)) {
          apiLogout();
          setUser(null);
          setToken(null);
        } else if (!cachedUser) {
          setUser(null);
        }
      } finally {
        setIsLoading(false);
      }
    }

    initAuth();
    return () => window.removeEventListener("ssc-auth-expired", handleExpiredSession);
  }, []);

  const handleLogin = async (payload: LoginPayload): Promise<User> => {
    const response = await apiLogin(payload);
    setToken(response.access_token);
    // apiLogin caches the response user for reconnect-safe auth initialization.
    setUser(response.user);
    return response.user;
  };

  const handleRegister = async (payload: RegisterPayload): Promise<User> => {
    const newUser = await apiRegister(payload);
    // Automatically log in the user after successful registration
    await handleLogin({
      email: payload.email,
      password: payload.password,
    });
    return newUser;
  };

  const handleLogout = (): void => {
    apiLogout();
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login: handleLogin,
        register: handleRegister,
        logout: handleLogout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
