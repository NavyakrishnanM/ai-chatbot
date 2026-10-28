import { Routes } from '@angular/router';
import { ChatComponent } from './features/chat/chat.component';

/**
 * App Routes
 *
 * CONCEPT — Lazy loading vs eager loading:
 * loadComponent: () => import(...)  → lazy: only loads the bundle when
 *                                      the user navigates to that route
 * component: ChatComponent          → eager: loaded at startup
 *
 * For Phase 2 we load eagerly (simpler).
 * Phase 7 will add auth guards: canActivate: [authGuard]
 */
export const routes: Routes = [
  {
    path: '',
    component: ChatComponent,
    title: 'DevAssist — AI Developer Assistant'
  }
];
