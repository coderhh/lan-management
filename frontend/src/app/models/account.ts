export class Account {
    public id?: string;
    public firstName?: string;
    public lastName?: string;
    public email?: string;
    public role?: string;
    public jwtToken?: string;
    /**
     *
     */
    constructor(id?: string, firstName?: string, lastName?: string, email?: string, role?: string, jwtToken?: string) {
      this.id = id;
      this.firstName = firstName;
      this.lastName = lastName;
      this.email = email;
      this.role = role;
      this.jwtToken = jwtToken;
    }

    static Create(){
      return this;
    }


}
