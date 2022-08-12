import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FirewallComponent } from './firewall/firewall.component';
import { HomeComponent } from './home/home.component';
import { VlanComponent } from './vlan/vlan.component';
import { AuthGuard } from './helpers/auth.guard';
import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { AccountsAddEditComponent } from './accounts-add-edit/accounts-add-edit.component';
import { FirewallAddEditComponent } from './firewall-add-edit/firewall-add-edit.component';
import { BindAddEditComponent } from './bind-add-edit/bind-add-edit.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'home', component: HomeComponent },
  { path: 'vlan', component: VlanComponent, canActivate: [AuthGuard] },
  { path: 'firewall', component: FirewallComponent, canActivate: [AuthGuard] },
  {
    path: 'firewall/edit/:id',
    component: FirewallAddEditComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'firewall/add',
    component: FirewallAddEditComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'vlan/edit/:id',
    component: BindAddEditComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'vlan/add',
    component: BindAddEditComponent,
    canActivate: [AuthGuard]
  },
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard] },
  {
    path: 'admin/edit/:id',
    component: AccountsAddEditComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'admin/add',
    component: AccountsAddEditComponent,
    canActivate: [AuthGuard]
  },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
