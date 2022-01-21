import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FirewallComponent } from './firewall/firewall.component';
import { HomeComponent } from './home/home.component';
import { NewRuleComponent } from './new-rule/new-rule.component';
import { NewBindComponent } from './new-bind/new-bind.component';
import { VlanComponent } from './vlan/vlan.component';
import { AuthGuard } from './helpers/auth.guard';
import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { AccountsAddEditComponent } from './accounts-add-edit/accounts-add-edit.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full'},
  { path: 'home', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'vlan/:id', component: VlanComponent },
  { path: 'firewall', component: FirewallComponent },
  { path: 'firewall/new', component: NewRuleComponent, canActivate: [AuthGuard]},
  { path: 'bind', component: NewBindComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent},
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard]},
  { path: 'admin/edit/:id', component: AccountsAddEditComponent },
  { path: 'admin/add', component: AccountsAddEditComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
