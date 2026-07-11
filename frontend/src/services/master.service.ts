import { api } from "@/lib/api";
import type { DomainResponse, SkillResponse, TechnologyResponse } from "@/types/api";

export const masterService = {
  // Skills
  listSkills: async () => (await api.get<SkillResponse[]>("/master/skills")).data,
  createSkill: async (name: string) =>
    (await api.post<SkillResponse>("/master/skills", { name })).data,
  searchSkills: async (q: string) =>
    (await api.get<SkillResponse[]>("/master/skills/search", { params: { q } })).data,
  // Domains
  listDomains: async () => (await api.get<DomainResponse[]>("/master/domains")).data,
  createDomain: async (name: string) =>
    (await api.post<DomainResponse>("/master/domains", { name })).data,
  searchDomains: async (q: string) =>
    (await api.get<DomainResponse[]>("/master/domains/search", { params: { q } })).data,
  // Technologies
  listTechnologies: async () =>
    (await api.get<TechnologyResponse[]>("/master/technologies")).data,
  createTechnology: async (name: string) =>
    (await api.post<TechnologyResponse>("/master/technologies", { name })).data,
  searchTechnologies: async (q: string) =>
    (await api.get<TechnologyResponse[]>("/master/technologies/search", { params: { q } })).data,
};
