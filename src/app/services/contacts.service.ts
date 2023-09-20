import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http'

import { Contact } from '../interfaces/contact';
import { MessagesService } from './messages.service';

@Injectable({
  providedIn: 'root'
})
export class ContactsService {
  url: string = 'http://127.0.0.1:5000';

  addContact(person: object): Observable<any> {
    return this.httpClient.post<any>(`${this.url}/api/add`, person);
  }

  getContacts(): Observable<Contact[]> {
    return this.httpClient.get<Contact[]>(`${this.url}/api/contacts`);
  }
  
  getFavorites(): Observable<Contact[]> {
    return this.httpClient.get<Contact[]>(`${this.url}/api/favorites`);
  }

  getContact(id: number): Observable<Contact> {
    return this.httpClient.get<Contact>(`${this.url}/api/contact/${id.toString()}`);
  }
  
  updateContact(id: number, contact: Contact): Observable<Contact> {
    return this.httpClient.put<Contact>(`${this.url}/api/update/${id.toString()}`, contact);
  }

  deleteContact(id: number): Observable<Contact> {
    return this.httpClient.delete<Contact>(`${this.url}/api/delete/${id.toString()}`);
  }

  isFavorite(id: number, favorite: object): Observable<Contact> {
    return this.httpClient.put<Contact>(`${this.url}/api/favorite/${id.toString()}`, favorite);
  }

  searchContacts(text: string, is_favorite_page: boolean): Observable<Contact[]> {
    if (!text.trim()) {
      if (is_favorite_page == true) {
        return this.httpClient.get<Contact[]>(`${this.url}/api/favorites`);
      } else {
        return this.httpClient.get<Contact[]>(`${this.url}/api/contacts`);
      }
    }
    return this.httpClient.get<Contact[]>(`${this.url}/api/search/?name=${text.toString()}`);
  }

  paginate(page: number, rows: number): Observable<Contact[]> {
    return this.httpClient.get<Contact[]>(`${this.url}/api/paginate/?page=${page.toString()}&rows=${rows.toString()}`);
  }

  dataValidation(name: string, email: string, telephone_number: string): boolean {
    if (!name) {
      this.messagesService.add(`Name missing`);
      return true;
    }

    if (!email && !telephone_number) {
      this.messagesService.add(`Email or Telephone Number must be set`);
      return true;
    }

    if (email) {
      const email_regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/;
      if (!email_regex.test(email)) {
        this.messagesService.add(`Email format incorrect`);
        return true;
      }
    }

    if (telephone_number) {
      const telephone_number_regex = /^\+?[0-9]{1,15}$/;
      if (!telephone_number_regex.test(telephone_number)) {
        this.messagesService.add(`Telephone Number format incorrect`);
        return true;
      }
    }

    return false
  }

  constructor(private httpClient: HttpClient, private messagesService: MessagesService) { }
}
