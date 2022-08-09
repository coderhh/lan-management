export class Account {
  public public_id?: string;
  public first_name?: string;
  public last_name?: string;
  public email?: string;
  public role?: string;
  public jwtToken?: string;
  public refreshToken?: string;
  /**
   *
   */
  constructor (id?: string, firstName?: string, lastName?: string, email?: string, role?: string, jwtToken?: string) {
    this.public_id = id;
    this.first_name = firstName;
    this.last_name = lastName;
    this.email = email;
    this.role = role;
    this.jwtToken = jwtToken;
  }

  static Create() {
    return this;
  }
}
