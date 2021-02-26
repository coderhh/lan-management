import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FirewallComponent } from './firewall/firewall.component';
import { HomeComponent } from './home/home.component';
import { NewRuleComponent } from './new-rule/new-rule.component';
import { NewBindComponent } from './new-bind/new-bind.component';
import { VlanComponent } from './vlan/vlan.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full'},
  { path: 'home', component: HomeComponent },
  { path: 'vlan/:id', component: VlanComponent },
  { path: 'firewall', component: FirewallComponent },
  { path: 'firewall/new', component: NewRuleComponent },
  { path: 'bind', component: NewBindComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
