import { Role } from './role';
export class Account {
    public id?: string;
    public title?: string;
    public firstName?: string;
    public lastName?: string;
    public email?: string;
    public role?: Role;
    public jwtToken?: string;
    /**
     *
     */
    constructor(id?: string, title?: string, firstName?: string, lastName?: string, email?: string, role?: Role, jwtToken?: string) {
      this.id = id;
      this.title = title;
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
