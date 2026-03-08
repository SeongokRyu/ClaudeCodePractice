/**
 * User type definition for the user service.
 */
export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Input type for creating a new user.
 * The id, createdAt, and updatedAt fields are generated automatically.
 */
export interface CreateUserInput {
  name: string;
  email: string;
}

/**
 * Input type for updating an existing user.
 * All fields are optional — only provided fields will be updated.
 */
export interface UpdateUserInput {
  name?: string;
  email?: string;
}
